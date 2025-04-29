document.getElementById('yourForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const prompt = document.getElementById('prompt').value;
    const image = document.getElementById('image').value;
  
    try {
      const response = await fetch('/api/critique', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt, image })
      });
  
      const result = await response.json();
      console.log(result);
      // Handle the result as needed
    } catch (error) {
      console.error('Error:', error);
    }
  });
  