// 千机AI聊天界面交互脚本 - 最终版本
document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    const userMessage = document.getElementById('userMessage');
    const sendBtn = document.getElementById('sendBtn');
    const fileInput = document.getElementById('fileInput');
    const mediaBtn = document.getElementById('mediaBtn');
    const dropZone = document.getElementById('dropZone');

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
                if (data.success) {
                    addMessage(`文件上传成功！分析结果：${data.analysis}`, 'bot');
                } else {
                    addMessage('文件上传失败，请重试。', 'bot');
                }
            })
            .catch(error => {
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
                const thinkingMessages = chatMessages.querySelectorAll('.bot-message');
                if (thinkingMessages.length > 0) {
                    thinkingMessages[thinkingMessages.length - 1].remove();
                }
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                console.error('Chat error:', error);
                // 移除"正在思考"消息
                const thinkingMessages = chatMessages.querySelectorAll('.bot-message');
                if (thinkingMessages.length > 0) {
                    thinkingMessages[thinkingMessages.length - 1].remove();
                }
                addMessage('抱歉，处理您的请求时出现了问题。请稍后重试。', 'bot');
            });
        }
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `<div class="message-content">${text.replace(/\n/g, '<br>')}</div>`;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // 表单提交
    const baziForm = document.getElementById('baziForm');
    if (baziForm) {
        baziForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const birthDate = document.getElementById('birthDate').value;
            const birthTime = document.getElementById('birthTime').value;
            const gender = document.getElementById('gender').value;
            const location = document.getElementById('location').value;
            
            if (!birthDate || !birthTime || !gender || !location) {
                alert('请填写完整信息');
                return;
            }
            
            const baziData = {
                birthDate: birthDate,
                birthTime: birthTime,
                gender: gender,
                location: location
            };
            
            addMessage(`快速八字分析请求：${JSON.stringify(baziData)}`, 'user');
            
            addMessage('千机AI正在分析...', 'bot');
            
            fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: `请分析以下八字信息：出生日期 ${birthDate}，出生时间 ${birthTime}，性别 ${gender}，出生地点 ${location}`
                })
            })
            .then(response => response.json())
            .then(data => {
                // 移除"正在分析"消息
                const thinkingMessages = chatMessages.querySelectorAll('.bot-message');
                if (thinkingMessages.length > 0) {
                    thinkingMessages[thinkingMessages.length - 1].remove();
                }
                addMessage(data.response, 'bot');
            })
            .catch(error => {
                console.error('Bazi analysis error:', error);
                // 移除"正在分析"消息
                const thinkingMessages = chatMessages.querySelectorAll('.bot-message');
                if (thinkingMessages.length > 0) {
                    thinkingMessages[thinkingMessages.length - 1].remove();
                }
                addMessage('八字分析失败，请重试。', 'bot');
            });
        });
    }
});