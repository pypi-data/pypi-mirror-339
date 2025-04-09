import { Streamlit } from "streamlit-component-lib";

// Debounce function to delay execution
function debounce(func, wait) {
  let timeout;
  return function (...args) {
    clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}

// Add event listener to watch for screen width changes
parent.addEventListener(
  "resize",
  debounce(() => {
    const screenWidth = parent.innerWidth;
    Streamlit.setComponentValue(screenWidth);
  }, 200)
);

// Set initial component value to current screen width
function onRender() {
  const screenWidth = parent.innerWidth;
  Streamlit.setComponentValue(screenWidth);
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender);
Streamlit.setComponentReady();
Streamlit.setFrameHeight(0);
