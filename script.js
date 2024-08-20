document.getElementById('student-form').addEventListener('submit', function(event) {
    event.preventDefault(); // prevent form submission

    var id = document.getElementById('id').value; 
    var name = document.getElementById('name').value;
    var age = parseInt(document.getElementById('age').value, 10);

    if (isNaN(age) || age <= 18) {
        var messageElement = document.getElementById('message');
        messageElement.textContent = 'Age must be greater than 18.';
        messageElement.className = 'message error';
        return; 
    }

    // Print form data to the console
    console.log("ID:", id);
    console.log("Name:", name);
    console.log("Age:", age);

    

    // Send form data to  backend
    fetch('http://localhost:8001/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ id:id, name: name, age: age }),
    })
    .then(response => response.json().then(data => {
        if (!response.ok) {
            throw new Error(data.message || 'Error submitting form');
        }
        return data;
    }))
    .then(data => {
        console.log('Success:', data);
        var messageElement = document.getElementById('message');
        messageElement.textContent = 'Form submitted successfully';
        messageElement.className = 'message success';
        // Clear the form inputs 
        document.getElementById('id').value = '';
        document.getElementById('name').value = '';
        document.getElementById('age').value = '';
    })
    .catch(error => {
        console.error('Error:', error);
        var messageElement = document.getElementById('message');
        messageElement.textContent = `Error submitting form: ${error.message}`;
        messageElement.className = 'message error';
    });
});
