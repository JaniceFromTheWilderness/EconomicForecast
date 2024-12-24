document.addEventListener('DOMContentLoaded', () => {
  // 驗證碼圖片
  const captchaImage = document.querySelector('img.captcha')
  // 重新整理 icon
  const icon = document.createElement('i')
  // 重新整理按鈕
  const refreshButton = document.createElement('a')
  // 是否在請求中
  let isFetching = false

  icon.classList.add('bi', 'bi-arrow-clockwise')
  refreshButton.href = 'JavaScript:void(0);'
  refreshButton.classList.add('captcha-refresh')
  refreshButton.appendChild(icon)
  captchaImage.parentNode.insertBefore(refreshButton, captchaImage.nextSibling)

  // 監聽重新整理點擊
  refreshButton.addEventListener('click', (event) => {
    event.preventDefault()

    /**
     * @type {Element|null} 表單
     */
    const form = event.target.closest('form')
    const url = `${location.origin}/captcha/refresh/`

    if (isFetching) {
      return
    }
    isFetching = true

    fetch(url, {
      headers: {
        'X-Requested-With': 'XMLHttpRequest'
      }
    })
      .then((response) => response.json())
      .then((json) => {
        const input = form.querySelector('input[name="captcha_0"]')
        input.value = json.key
        captchaImage.src = json.image_url
      })
      .catch((error) => {
        console.log(error)
      })
      .finally(() => {
        isFetching = false
      })
  })
})