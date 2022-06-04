/* Please don't change this file. To implement custom js, use config! */

// themes
var themes = {}
var default_theme = "none"
function apply_theme() {
  theme = window.location.href.split("?theme=")[1] || default_theme || "none"
  console.log("applying theme: " + theme)
  if (theme!="none") {
    var link = document.createElement("link")
    link.href = themes[theme] || theme
    link.rel = "stylesheet"
    document.head.appendChild(link)
  }
}
