import { Streamlit } from "streamlit-component-lib";

const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    mutation.removedNodes.forEach((node) => {
      if (node.querySelector('[role="dialog"]')) {
        // console.log("Dialog removed:", node);
        Streamlit.setComponentValue(true);
      }
    });
  });
});

// observe the root element of parent window
observer.observe(parent.document.getElementById("root"), {
  childList: true,
  subtree: true,
});

Streamlit.setComponentReady();
Streamlit.setFrameHeight(0);
