// 千机AI聊天界面交互脚本 - 修复版本
document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chatMessages');
    const messageInput = document.getElementById('userMessage');
    const sendButton = document.getElementById('sendBtn');
    const uploadButton = document.getElementById('mediaBtn');
    const fileInput = document.getElementById('fileInput');
    const dropZone = document.getElementById('dropZone');
    
    // 确保聊天容器可以滚动
    if (chatContainer) {
        chatContainer.style.overflowY = 'auto';
        chatContainer.style.maxHeight = 'calc(100vh - 300px)';
    }
    
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
    uploadButton.addEventListener('click', () => fileInput.click());
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
                removeLastBotMessage();
                if (data.success) {
                    addMessage(`文件上传成功！分析结果：${data.analysis}`, 'bot');
                } else {
                    addMessage('文件上传失败，请重试。', 'bot');
                }
            })
            .catch(error => {
                removeLastBotMessage();
                addMessage('上传过程中出现错误。', 'bot');
                console.error('Upload error:', error);
            });
        }
    }

    // 聊天功能
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    function sendMessage() {
        const message = messageInput.value.trim();
        if (message) {
            addMessage(message, 'user');
            messageInput.value = '';
            sendMessageToAI(message);
        }
    }

    function addMessage(text, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `<div class="message-content">${text.replace(/\n/g, '<br>')}</div>`;
        chatContainer.appendChild(messageDiv);
        scrollToBottom();
    }
    
    function removeLastBotMessage() {
        const botMessages = chatContainer.querySelectorAll('.bot-message');
        if (botMessages.length > 0) {
            botMessages[botMessages.length - 1].remove();
        }
    }
    
    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    function sendMessageToAI(message) {
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
            removeLastBotMessage();
            addMessage(data.response, 'bot');
        })
        .catch(error => {
            console.error('Chat error:', error);
            removeLastBotMessage();
            addMessage('抱歉，处理您的请求时出现了问题。请稍后重试。', 'bot');
        });
    }

    // 表单提交 - 修复数据提取
    const baziForm = document.getElementById('baziForm');
    if (baziForm) {
        baziForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // 正确获取表单数据
            const birthDate = document.getElementById('birthDate').value;
            const birthTime = document.getElementById('birthTime').value;
            const gender = document.getElementById('gender').value;
            const location = document.getElementById('location').value;
            
            console.log('Form data:', {birthDate, birthTime, gender, location});
            
            if (!birthDate || !birthTime || !gender || !location) {
                addMessage('请填写完整的八字信息！', 'bot');
                return;
            }
            
            // 格式化显示
            const timeLabels = {
                '23:00': '子时 (23:00-01:00)',
                '01:00': '丑时 (01:00-03:00)',
                '03:00': '寅时 (03:00-05:00)',
                '05:00': '卯时 (05:00-07:00)',
                '07:00': '辰时 (07:00-09:00)',
                '09:00': '巳时 (09:00-11:00)',
                '11:00': '午时 (11:00-13:00)',
                '13:00': '未时 (13:00-15:00)',
                '15:00': '申时 (15:00-17:00)',
                '17:00': '酉时 (17:00-19:00)',
                '19:00': '戌时 (19:00-21:00)',
                '21:00': '亥时 (21:00-23:00)'
            };
            
            const displayTime = timeLabels[birthTime] || birthTime;
            const genderText = gender === 'male' ? '男' : '女';
            
            const userData = `出生日期: ${birthDate}, 出生时间: ${displayTime}, 性别: ${genderText}, 出生地点: ${location}`;
            addMessage(`快速八字分析请求：${userData}`, 'user');
            
            // 发送完整数据给AI
            const fullMessage = `请基于以下八字信息进行专业命理分析：
出生日期: ${birthDate}
出生时间: ${birthTime}
性别: ${gender}
出生地点: ${location}

请提供详细的命盘分析、五行格局、用神建议和人生运势预测。`;
            
            sendMessageToAI(fullMessage);
        });
    }
    
    // 初始化时确保滚动到底部
    setTimeout(() => {
        scrollToBottom();
    }, 100);
});