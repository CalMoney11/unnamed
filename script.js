form.addEventListener('submit', async (e) => {
  e.preventDefault();

  const prompt = document.getElementById('art').value;
  const style = document.getElementById('style').value;
  const file = fileInput.files[0];

  if (!file) {
    warningBox.textContent = "Please upload an image file.";
    return;
  }

  const formData = new FormData();
  formData.append('image', file);  // ✅ must match app.py
  formData.append('style', style);
  formData.append('prompt', prompt);

  responseBox.textContent = "Analyzing artwork... Please wait.";

  try {
    const res = await fetch('https://unnamed-94574790644.us-west1.run.app/api/critique', {
      method: 'POST',
      body: formData,
      // ❌ DO NOT manually set content-type; let the browser do it for multipart/form-data
    });

    const data = await res.json();

    if (!res.ok) {
      console.error("Server returned error response:", data);
      throw new Error(`Server returned ${res.status}: ${data.error}`);
    }

    responseBox.textContent = data.critique || JSON.stringify(data, null, 2);
  } catch (err) {
    console.error("Submission error:", err);
    responseBox.textContent = "An error occurred while submitting your artwork. Check the console for details.";
  }
});
