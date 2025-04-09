document.addEventListener('DOMContentLoaded', function () {
    // Only run on admin change form
    if (!document.getElementById('content-main') || !document.querySelector('.change-form')) {
        return;
    }

    // Get the current URL path to extract info
    const path = window.location.pathname;
    const adminMatch = path.match(/\/admin\/(\w+)\/(\w+)\/(\w+)\/change\//);

    if (!adminMatch) {
        return;
    }

    const appLabel = adminMatch[1];
    const modelName = adminMatch[2];
    const objectId = adminMatch[3];

    // Track the last modified timestamp to detect changes
    let lastModifiedTimestamp = null;

    // Create a warning banner for users without edit permissions (hidden by default)
    const warningBanner = document.createElement('div');
    warningBanner.id = 'edit-lock-warning';
    warningBanner.style.display = 'none';
    warningBanner.style.padding = '15px';
    warningBanner.style.margin = '0';
    warningBanner.style.fontSize = '15px';
    warningBanner.style.fontWeight = 'bold';
    warningBanner.style.position = 'fixed';
    warningBanner.style.top = '0';
    warningBanner.style.left = '0';
    warningBanner.style.right = '0';
    warningBanner.style.zIndex = '1000';
    warningBanner.style.textAlign = 'center';
    warningBanner.style.color = '#721c24';
    warningBanner.style.backgroundColor = '#f8d7da';
    warningBanner.style.borderBottom = '1px solid #f5c6cb';

    // Add warning banner to the body (so it stays fixed at top)
    document.body.appendChild(warningBanner);

    // Create user avatars container
    const userAvatarsContainer = document.createElement('div');
    userAvatarsContainer.id = 'user-avatars-container';
    userAvatarsContainer.style.position = 'fixed';
    userAvatarsContainer.style.top = '5px';
    userAvatarsContainer.style.right = '10px';
    userAvatarsContainer.style.zIndex = '1001';
    userAvatarsContainer.style.display = 'flex';
    userAvatarsContainer.style.flexDirection = 'row-reverse'; // Right to left
    userAvatarsContainer.style.gap = '5px';

    // Add user avatars container to the body
    document.body.appendChild(userAvatarsContainer);

    // Variables to track editing state
    let canEdit = false;
    let currentEditor = null;
    let currentEditorName = null;
    let myUserId = null;
    let myUsername = null;
    let joinTimestamp = null;
    let refreshTimer = null;
    let reconnectTimer = null;
    let activeUsers = {}; // will now store {id: {username, email}}
    let reconnectAttempts = 0;
    const MAX_RECONNECT_ATTEMPTS = 5;
    let socket = null;

    // Helper function to get UTC ISO timestamp
    function getUTCTimestamp() {
        return new Date().toISOString();
    }

    // Helper function to compare timestamps
    function isTimeAfter(time1, time2) {
        return new Date(time1) > new Date(time2);
    }

    function connectWebSocket() {
        if (socket) {
            // Close existing socket properly
            socket.onclose = null; // Remove reconnect logic
            socket.close();
        }

        var base_part = location.hostname + (location.port ? ':' + location.port : '');
        let wssSource = `/admin/collaboration/${appLabel}/${modelName}/${objectId}/`
        if (location.protocol === 'https:') {
            wssSource = "wss://" + base_part + wssSource;
        } else if (location.protocol === 'http:') {
            wssSource = "ws://" + base_part + wssSource;
        }

        socket = new WebSocket(wssSource);

        socket.onopen = function (e) {
            console.log('WebSocket connection established');
            reconnectAttempts = 0; // Reset counter on successful connection

            if (refreshTimer) {
                clearTimeout(refreshTimer);
                refreshTimer = null;
            }
        };

        socket.onmessage = function (e) {
            const data = JSON.parse(e.data);

            if (data.type === 'user_joined') {
                handleUserJoined(data);
            } else if (data.type === 'user_left') {
                handleUserLeft(data);
            } else if (data.type === 'editor_status') {
                handleEditorStatus(data);
            } else if (data.type === 'content_updated') {
                handleContentUpdated(data);
            } else if (data.type === 'lock_released') {
                handleLockReleased(data);
            }
        };

        socket.onclose = function (e) {
            console.log('WebSocket connection closed');

            // Try to reconnect a limited number of times if not deliberately closed
            if (!window.isNavigatingAway && reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                reconnectAttempts++;
                const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000); // Exponential backoff with 30s max

                showWarningMessage(`Connection lost. Trying to reconnect... (Attempt ${reconnectAttempts})`);

                if (reconnectTimer) {
                    clearTimeout(reconnectTimer);
                }

                reconnectTimer = setTimeout(connectWebSocket, delay);
            } else if (reconnectAttempts >= MAX_RECONNECT_ATTEMPTS) {
                showWarningMessage('Connection lost. Please refresh the page manually.');
            }
        };

        socket.onerror = function (e) {
            console.error('WebSocket error:', e);
        };
    }

    // Initial connection
    connectWebSocket();

    function handleUserJoined(data) {
        if (!myUserId) {
            myUserId = data.user_id;
            myUsername = data.username;
            joinTimestamp = new Date(data.timestamp);
            lastModifiedTimestamp = data.last_modified;

            socket.send(JSON.stringify({
                'type': 'request_editor_status',
                'timestamp': getUTCTimestamp()
            }));
        } else if (data.user_id !== myUserId) {
            // Store user info with email
            activeUsers[data.user_id] = {
                username: data.username,
                email: data.email
            };

            // Add avatar for new user
            addUserAvatar(data.user_id, data.username, data.email);
        }
    }

    function handleUserLeft(data) {
        if (data.user_id in activeUsers) {
            delete activeUsers[data.user_id];
            // Remove user avatar
            const userAvatar = document.getElementById(`user-avatar-${data.user_id}`);
            if (userAvatar) {
                userAvatar.remove();
            }
        }

        if (data.user_id === currentEditor && currentEditor !== myUserId) {
            showWarningMessage('The editor has left. The page will refresh shortly to allow editing.');
            clearTimeout(refreshTimer);
            refreshTimer = setTimeout(function () {
                window.location.reload();
            }, 2000);
        }
    }

    function handleEditorStatus(data) {
        currentEditor = data.editor_id;
        currentEditorName = data.editor_name;

        // Update all existing avatars to reflect editor status
        updateAvatarEditorStatus();

        if (currentEditor === myUserId) {
            canEdit = true;
            showSuccessMessage(`You are in editor mode.`);
            enableForm();
        } else if (currentEditor) {
            canEdit = false;
            showWarningMessage(`This page is being edited by ${data.editor_name}. You cannot make changes until they leave.`);
            disableForm();
        } else {
            socket.send(JSON.stringify({
                'type': 'claim_editor',
                'timestamp': getUTCTimestamp()
            }));
        }
    }

    function handleContentUpdated(data) {
        if (currentEditor !== myUserId) {
            showWarningMessage('The content has been updated. The page will refresh shortly.');

            if (!lastModifiedTimestamp || isTimeAfter(data.timestamp, lastModifiedTimestamp)) {
                lastModifiedTimestamp = data.timestamp;
                clearTimeout(refreshTimer);
                refreshTimer = setTimeout(function () {
                    window.location.reload();
                }, 2000);
            }
        }
    }

    function handleLockReleased(data) {
        if (currentEditor !== myUserId) {
            showWarningMessage('The editor has finished editing. The page will refresh to allow you to edit.');

            clearTimeout(refreshTimer);
            refreshTimer = setTimeout(function () {
                window.location.reload();
            }, 2000);
        }
    }

    function showWarningMessage(message) {
        warningBanner.textContent = message;
        warningBanner.style.display = 'block';
        warningBanner.style.backgroundColor = '#f8d7da';
        warningBanner.style.color = '#721c24';
        warningBanner.style.borderBottom = '1px solid #f5c6cb';

        // Adjust body padding to prevent content from being hidden under the warning
        document.body.style.paddingTop = warningBanner.offsetHeight + 'px';
    }

    function showSuccessMessage(message) {
        warningBanner.textContent = message;
        warningBanner.style.display = 'block';
        warningBanner.style.backgroundColor = '#d4edda';
        warningBanner.style.color = '#155724';
        warningBanner.style.borderBottom = '1px solid #c3e6cb';

        // Adjust body padding to prevent content from being hidden under the warning
        document.body.style.paddingTop = warningBanner.offsetHeight + 'px';
    }

    function hideWarningMessage() {
        warningBanner.style.display = 'none';
        document.body.style.paddingTop = '0';
    }

    function addUserAvatar(userId, username, email) {
        // Check if avatar already exists
        if (document.getElementById(`user-avatar-${userId}`)) {
            return;
        }

        // Create avatar element
        const avatar = document.createElement('div');
        avatar.id = `user-avatar-${userId}`;
        avatar.className = 'user-avatar';
        avatar.setAttribute('data-user-id', userId);
        avatar.setAttribute('title', `${username}`);

        // Avatar styling
        avatar.style.width = '36px';
        avatar.style.height = '36px';
        avatar.style.borderRadius = '50%';
        avatar.style.display = 'flex';
        avatar.style.alignItems = 'center';
        avatar.style.justifyContent = 'center';
        avatar.style.fontWeight = 'bold';
        avatar.style.fontSize = '16px';
        avatar.style.color = '#fff';
        avatar.style.textTransform = 'uppercase';
        avatar.style.position = 'relative';

        // Set background color - editor gets different color
        if (userId === currentEditor) {
            avatar.style.backgroundColor = '#28a745'; // Green for editor
            avatar.style.border = '2px solid #20c997';
        } else {
            avatar.style.backgroundColor = '#007bff'; // Blue for viewers
            avatar.style.border = '2px solid #0056b3';
        }

        // Add first letter of username
        avatar.textContent = username.charAt(0);

        // Create and append tooltip
        const tooltip = document.createElement('div');
        tooltip.className = 'avatar-tooltip';
        tooltip.textContent = `${username}`;
        tooltip.style.position = 'absolute';
        tooltip.style.bottom = '-30px';
        tooltip.style.right = '0';
        tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
        tooltip.style.color = '#fff';
        tooltip.style.padding = '5px 10px';
        tooltip.style.borderRadius = '3px';
        tooltip.style.fontSize = '12px';
        tooltip.style.whiteSpace = 'nowrap';
        tooltip.style.display = 'none';
        tooltip.style.zIndex = '1002';

        avatar.appendChild(tooltip);

        // Show/hide tooltip on hover
        avatar.addEventListener('mouseenter', () => {
            tooltip.style.display = 'block';
        });

        avatar.addEventListener('mouseleave', () => {
            tooltip.style.display = 'none';
        });

        // Add avatar to container
        userAvatarsContainer.appendChild(avatar);
    }

    function updateAvatarEditorStatus() {
        // Update all avatars to reflect current editor status
        document.querySelectorAll('.user-avatar').forEach(avatar => {
            const userId = avatar.getAttribute('data-user-id');

            if (userId == currentEditor) {
                avatar.style.backgroundColor = '#28a745'; // Green for editor
                avatar.style.border = '2px solid #20c997';
            } else {
                avatar.style.backgroundColor = '#007bff'; // Blue for viewers
                avatar.style.border = '2px solid #0056b3';
            }
        });
    }

    function disableForm() {
        const form = document.querySelector('#content-main form');
        if (!form) return;

        const elements = form.querySelectorAll('input, select, textarea, button');
        elements.forEach(element => {
            element.disabled = true;
            element.style.opacity = '0.7';
            element.style.cursor = 'not-allowed';
        });

        const submitRow = document.querySelector('.submit-row');
        if (submitRow) {
            submitRow.style.display = 'none';
        }

        document.querySelectorAll('a.addlink, a.changelink, a.deletelink').forEach(link => {
            link.style.pointerEvents = 'none';
            link.style.opacity = '0.5';
        });
    }

    function enableForm() {
        const form = document.querySelector('#content-main form');
        if (!form) return;

        const elements = form.querySelectorAll('input, select, textarea, button');
        elements.forEach(element => {
            element.disabled = false;
            element.style.opacity = '';
            element.style.cursor = '';
        });

        const submitRow = document.querySelector('.submit-row');
        if (submitRow) {
            submitRow.style.display = 'flex';
        }

        document.querySelectorAll('a.addlink, a.changelink, a.deletelink').forEach(link => {
            link.style.pointerEvents = '';
            link.style.opacity = '';
        });

        form.addEventListener('submit', function () {
            socket.send(JSON.stringify({
                'type': 'content_updated',
                'timestamp': getUTCTimestamp()
            }));
        });

        const saveButtons = document.querySelectorAll('input[name="_continue"], input[name="_save"]');
        saveButtons.forEach(button => {
            button.addEventListener('click', function () {
                window.isNavigatingAway = true;
                socket.send(JSON.stringify({
                    'type': 'release_lock'
                }));
            });
        });
    }

    // Send heartbeat every 30 seconds to maintain our editor status
    const heartbeatInterval = setInterval(function () {
        if (canEdit && socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                'type': 'heartbeat'
            }));
        }
    }, 30000);

    // Clean up when navigating away
    window.addEventListener('beforeunload', function () {
        window.isNavigatingAway = true;
        clearInterval(heartbeatInterval);
        clearTimeout(refreshTimer);
        clearTimeout(reconnectTimer);

        if (canEdit && socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                'type': 'release_lock'
            }));
        }

        if (socket) {
            socket.onclose = null; // Remove reconnect logic
            socket.close();
        }
    });
});