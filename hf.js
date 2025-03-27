async function query(data) {
  const response = await fetch(
    "https://api-inference.huggingface.co/spaces/arkankau/dau",
    {
      headers: {
        Authorization: "Bearer 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",
        "Content-Type": "application/json"
      },
      method: "POST",
      body: JSON.stringify(data),
    }
  );
  const result = await response.json();
  return result;
}

query({ inputs: "The Empire State Building is 1,454 feet tall." }).then((response) => {
  console.log(response);
});

document.querySelector('.chatbot-iframe').addEventListener('load', function () {
  const iframe = this;
  try {
    // Dynamically adjust the height based on the content inside the iframe
    iframe.style.height = iframe.contentWindow.document.body.scrollHeight + 'px';
  } catch (error) {
    console.error("Unable to adjust iframe height:", error);
  }
});