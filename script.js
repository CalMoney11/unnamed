document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('critique-form');
  const fileInput = document.getElementById('file');
  const preview = document.getElementById('preview');
  const responseBox = document.getElementById('response');
  const warningBox = document.getElementById('file-warning');

  if (!form) return;

  // Show image preview
  fileInput.addEventListener('change', () => {
    const file = fileInput.files[0];
    if (file && file.size > 5 * 1024 * 1024) {
      warningBox.textContent = "File exceeds 5MB limit.";
      fileInput.value = "";
      preview.style.display = "none";
      return;
    }

    warningBox.textContent = "";

    const reader = new FileReader();
    reader.onload = e => {
      preview.src = e.target.result;
      preview.style.display = "block";
    };
    reader.readAsDataURL(file);
  });

  // Handle form submission
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
    formData.append('prompt', prompt);
    formData.append('style', style);
    formData.append('image', file);

    responseBox.textContent = "Analyzing artwork... Please wait.";

    try {
      const res = await fetch('https://unnamed-94574790644.us-west1.run.app/api/critique', {
        method: 'POST',
        body: formData
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
});
