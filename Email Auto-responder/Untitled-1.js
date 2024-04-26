const endpoint = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent';
var apikey = "AIzaSyDDFB8cWAHXb63OajbvVvBBmlyT9ZLmluI";
// Define the data to be sent in the API request
const requestData = {
  contents: [
    {
      parts: [
        {
          text: "Write a story about a magic backpack"
        }
      ]
    }
  ]
};

// Perform the API call using the fetch API
fetch(endpoint + '?key=' + apikey, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(requestData)
})
.then(response => response.json())
.then(data => {
  // Process the response data here
  if (data.candidates && data.candidates.length > 0 && data.candidates[0].content) {
    const story = data.candidates[0].content; // This might need adjustment based on the actual structure
    console.log('Generated Story:', story);
  } else {
    console.log('No story generated or response structure is different than expected.');
  }
})
.catch((error) => {
  // Handle any errors here
  console.error('Error:', error);
});
