async function sendData(data) {
    try {
        const response = await fetch('http://127.0.0.1:8080/api/movie', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) 
        });

        return response;
    }
    catch (err) {
        console.error('Error:', err);
    }
}

browser.runtime.onMessage.addListener(async msg => {
    if(msg.command === "scrape") {
        await sendData(msg.data)
    }
})

