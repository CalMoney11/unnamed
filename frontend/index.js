// this is the JavaScript code for the frontend of the critique app the runs on github pages
// This code handles the form submission and sends the data to the Cloud Function

// Replace this with your actual deployed Cloud Function URL
const apiUrl = "https://us-central1-ai-art-critique-460706.cloudfunctions.net/generate_art_critique"; // do i need this? and APIurl?

document.getElementById("critique-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const formData = new FormData();
  formData.append("prompt", document.getElementById("art").value);
  formData.append("style", document.getElementById("style").value);
  const file = document.getElementById("file").files[0];
  formData.append("file", file);

  document.getElementById("response").textContent = "Processing...";

  try {
    const response = await fetch(apiUrl, {
      method: "POST",
      body: formData,
    });

    const result = await response.json();
    document.getElementById("response").textContent = result.response || result.error;
  } catch (err) {
    document.getElementById("response").textContent = "Something went wrong: " + err.message;
  }
});
