// Toast 提示管理（全局）
let currentToast = null;
function showToast(message) {
    // 如果已有 Toast，先移除
    if (currentToast) {
        document.body.removeChild(currentToast);
    }

    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.textContent = message;
    document.body.appendChild(toast);

    currentToast = toast;
}

function hideToast() {
    if (currentToast) {
        document.body.removeChild(currentToast);
        currentToast = null;
    }
}

// 下载歌曲的JavaScript函数
function downloadSong(event) {
    // 获取点击的按钮元素
    const button = event.currentTarget;
    // 从按钮的data属性中获取索引i
    const index = parseInt(button.getAttribute('data-index'));

    // 1. 显示 "正在准备下载" 提示
    showToast("正在准备下载音频...");
    // 2. 禁用按钮，防止重复点击
    button.disabled = true;

    // 发送GET请求到后端
    fetch(`/get_audio_download/${index}`)
      .then(async response => {
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        //  3. 移除 "正在准备" 提示，改为进度条
        hideToast();

        // 获取文件名（从Content-Disposition或自定义）
        //const contentDisposition = response.headers.get('Content-Disposition');
        const filename = "audio.m4a"//contentDisposition?.match(/filename="?(.+?)"?$/)?.[1] || `audio_${index}.mp3`;

        // 创建流式读取器
        const reader = response.body.getReader();
        const chunks = [];
        let receivedLength = 0;
        const contentLength = +response.headers.get('Content-Length');

        // 显示进度条（放在页面顶部）
        const progressBar = document.createElement('div');
        progressBar.style.width = '100%';
        progressBar.style.backgroundColor = '#ddd';
        progressBar.style.margin = '0';
        progressBar.style.position = 'fixed';
        progressBar.style.top = '0';
        progressBar.style.left = '0';
        progressBar.style.zIndex = '1000';
        document.body.insertBefore(progressBar, document.body.firstChild);

        // 进度条内部填充元素
        const progressFill = document.createElement('div');
        progressFill.style.height = '20px';
        progressFill.style.backgroundColor = '#4CAF50';
        progressFill.style.width = '0%';
        progressFill.style.transition = 'width 0.3s';
        progressFill.style.textAlign = 'center';
        progressFill.style.color = 'white';
        progressFill.style.lineHeight = '20px';
        progressBar.appendChild(progressFill);

        // 逐块读取数据
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          chunks.push(value);
          receivedLength += value.length;

          // 更新进度（可选）
          if (contentLength) {
            const percent = Math.round((receivedLength / contentLength) * 100);
            progressFill.style.width = `${percent}%`;
            progressFill.textContent = `${percent}%`;
          }
        }

        // 合并数据并触发下载
        const blob = new Blob(chunks);
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();

        // 清理
        setTimeout(() => {
          document.body.removeChild(a);
          document.body.removeChild(progressBar);
          URL.revokeObjectURL(url);
        }, 100);
      })
      .catch(error => {
        console.error('下载失败:', error);
        alert(`下载失败: ${error.message}`);
      })
      .finally(() => {
        //4. 无论成功或失败，重新启用按钮
        button.disabled = false;
      });
}

// 视频下载函数
function downloadVideo(event) {
    // 1. 显示 "正在准备下载" 提示
    showToast("正在准备下载音频...");
    // 2. 禁用按钮，防止重复点击
    button.disabled = true;

    // 获取点击的按钮元素
    const button = event.currentTarget;
    // 从按钮的data属性中获取索引i
    const index = parseInt(button.getAttribute('data-index'))

    // 发送GET请求到后端
    fetch(`/get_video_download/${index}`)
      .then(async response => {
        //  3. 移除 "正在准备" 提示，改为进度条
        hideToast();

        if (!response.ok) throw new Error(`HTTP ${response.status}`);

        // 获取文件名（从Content-Disposition或自定义）
        //const contentDisposition = response.headers.get('Content-Disposition');
        const filename = "download.mp4"      //contentDisposition?.match(/filename="?(.+?)"?$/)?.[1] || `audio_${index}.mp3`;

        // 创建流式读取器
        const reader = response.body.getReader();
        const chunks = [];
        let receivedLength = 0;
        const contentLength = +response.headers.get('Content-Length');

        // 显示进度条（放在页面顶部）
        const progressBar = document.createElement('div');
        progressBar.style.width = '100%';
        progressBar.style.backgroundColor = '#ddd';
        progressBar.style.margin = '0';
        progressBar.style.position = 'fixed';
        progressBar.style.top = '0';
        progressBar.style.left = '0';
        progressBar.style.zIndex = '1000';
        document.body.insertBefore(progressBar, document.body.firstChild);

        // 进度条内部填充元素
        const progressFill = document.createElement('div');
        progressFill.style.height = '20px';
        progressFill.style.backgroundColor = '#4CAF50';
        progressFill.style.width = '0%';
        progressFill.style.transition = 'width 0.3s';
        progressFill.style.textAlign = 'center';
        progressFill.style.color = 'white';
        progressFill.style.lineHeight = '20px';
        progressBar.appendChild(progressFill);

        // 逐块读取数据
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          chunks.push(value);
          receivedLength += value.length;

          // 更新进度（可选）
          if (contentLength) {
            const percent = Math.round((receivedLength / contentLength) * 100);
            progressFill.style.width = `${percent}%`;
            progressFill.textContent = `${percent}%`;
          }
        }

        // 合并数据并触发下载
        const blob = new Blob(chunks);
        const url = URL.createObjectURL(blob);

        const a = document.createElement('a');
        a.href = url;
        a.download = filename;
        a.style.display = 'none';
        document.body.appendChild(a);
        a.click();

        // 清理
        setTimeout(() => {
          document.body.removeChild(a);
          document.body.removeChild(progressBar);
          URL.revokeObjectURL(url);
        }, 100);
      })
      .catch(error => {
        console.error('下载失败:', error);
        alert(`下载失败: ${error.message}`);
      })
      .finally(() => {
        //4. 无论成功或失败，重新启用按钮
        button.disabled = false;
      });
}



// 为所有下载按钮添加点击事件监听器
document.addEventListener('DOMContentLoaded', function() {
    //处理视频下载
    const downloadButtons = document.querySelectorAll('.download-btn');
    downloadButtons.forEach(button => {
        button.addEventListener('click', downloadSong);
    });

    // 处理视频下载按钮
    const videoDownloadButtons = document.querySelectorAll('.video-download-btn');
    videoDownloadButtons.forEach(button => {
        button.addEventListener('click', downloadVideo);  // 改为视频下载函数
    });
});