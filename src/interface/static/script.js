// 千机AI聊天界面交互脚本 - 完全验证版本
document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userMessage = document.getElementById('userMessage');
    const sendBtn = document.getElementById('sendBtn');
    const mediaBtn = document.getElementById('mediaBtn');
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('dropZone');
    const baziForm = document.getElementById('baziForm');

    // 拖拽上传功能
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        dropZone.classList.add('highlight');
    }

    function unhighlight() {
        dropZone.classList.remove('highlight');
    }

    dropZone.addEventListener('drop', handleDrop, false);
    mediaBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', handleFiles);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        handleFiles({target: {files: files}});
    }

    function handleFiles(e) {
        const files = e.target.files;
        if (files.length > 0) {
            const file = files[0];
            const formData = new FormData();
            formData.append('file', file);
            
            addMessage('正在上传文件...', 'bot');
            
            fetch('/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                // 移除"正在上传"消息
                const uploadMsg = chatMessages.querySelector('.bot-message:last-child');
                if (uploadMsg) uploadMsg.remove();
                
                if (data.success) {
                    addMessage(`文件上传成功！分析结果：${data.analysis}`, 'bot');
                } else {
                    addMessage('文件上传失败，请重试。', 'bot');
                }
            })
            .catch(error => {
                const uploadMsg = chatMessages.querySelector('.bot-message:last-child');
                if (uploadMsg) uploadMsg.remove();
                addMessage('上传过程中出现错误。', 'bot');
                console.error('Upload error:', error);
            });
        }
    }

    // 聊天功能
    sendBtn.addEventListener('click', sendMessage);
    userMessage.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const message = userMessage.value.trim();
        if (message) {
            addMessage(message, 'user');
            userMessage.value = '';
            
            addMessage('千机AI正在思考...', 'bot');
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({message: message})
            })
            .then(response => response.json())
            .then(data => {
                // 移除"正在思考"消息
                const thinkingMsg = chatMessages.querySelector('.bot-message:last-child');
                if (thinkingMsg) thinkingMsg.remove();
                
                addMessage(data.response, 'bot');
                scrollToBottom();
            })
            .catch(error => {
                const thinkingMsg = chatMessages.querySelector('.bot-message:last-child');
                if (thinkingMsg) thinkingMsg.remove();
                addMessage('抱歉，处理您的请求时出现了问题。请稍后重试。', 'bot');
                console.error('Chat error:', error);
                scrollToBottom();
            });
        }
    }

    // 表单提交
    baziForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const birthDate = document.getElementById('birthDate').value;
        const birthTime = document.getElementById('birthTime').value;
        const gender = document.getElementById('gender').value;
        const location = document.getElementById('location').value;
        
        if (!birthDate || !birthTime || !gender || !location) {
            alert('请填写完整信息！');
            return;
        }
        
        const baziData = {
            birthDate: birthDate,
            birthTime: birthTime,
            gender: gender,
            location: location
        };
        
        addMessage(`快速八字分析请求：出生日期 ${birthDate}，出生时间 ${birthTime}，性别 ${gender}，出生地点 ${location}`, 'user');
        
        addMessage('千机AI正在分析...', 'bot');
        
        fetch('/bazi', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(baziData)
        })
        .then(response => response.json())
        .then(data => {
            // 移除"正在分析"消息
            const analyzingMsg = chatMessages.querySelector('.bot-message:last-child');
            if (analyzingMsg) analyzingMsg.remove();
            
            addMessage(data.response, 'bot');
            scrollToBottom();
        })
        .catch(error => {
            const analyzingMsg = chatMessages.querySelector('.bot-message:last-child');
            if (analyzingMsg) analyzingMsg.remove();
            addMessage('八字分析失败，请重试。', 'bot');
            console.error('Bazi error:', error);
            scrollToBottom();
        });
    });

    // 辅助函数
    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `<div class="message-content">${text.replace(/\n/g, '<br>')}</div>`;
        chatMessages.appendChild(messageDiv);
        scrollToBottom();
    }

    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});