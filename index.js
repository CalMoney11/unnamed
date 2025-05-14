const functions = require('firebase-functions');
const axios = require('axios');
const cors = require('cors')({ origin: true });

exports.api = functions.https.onRequest((req, res) => {
  cors(req, res, async () => {
    if (req.path === '/critique' && req.method === 'POST') {
      const { prompt, image } = req.body;
      const apiKey = functions.config().openai.key;

      try {
        const response = await axios.post(
          'https://api.openai.com/v1/chat/completions',
          {
            model: 'gpt-4-vision-preview',
            messages: [
              {
                role: 'user',
                content: [
                  { type: 'text', text: prompt },
                  { type: 'image_url', image_url: { url: image } }
                ]
              }
            ],
            max_tokens: 500
          },
          {
            headers: {
              'Authorization': `Bearer ${apiKey}`,
              'Content-Type': 'application/json'
            }
          }
        );
        res.status(200).json(response.data);
      } catch (error) {
        console.error('OpenAI API error:', error);
        res.status(500).send('Error processing request');
      }
    } else {
      res.status(404).send('Not Found');
    }
  });
});
