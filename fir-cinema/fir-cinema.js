(() => {
    if (window.hasRun) {
        return;
    }
    window.hasRun = true;

    function isValidUrl(url) {
        return url.includes("https://www.allocine.fr/film/");
        
    }

    function getDuration(divElement) {
        const durationMatch = divElement.innerHTML.match(/>([^<]+)<\/span>([^<]*)/);

        if(durationMatch) {
            return durationMatch[2].trim();
        }

        return null;
    }


    function scrapPage() {
        /*
        *   Metabody datas
        */
        const metaBody = document.querySelector(".meta-body");

        const title = document.querySelector(".titlebar-title").innerHTML;

        const metaBodyDirection = metaBody.querySelectorAll(".meta-body-direction");

        const directorCointainer = metaBodyDirection[0];
        const directorsElements = directorCointainer.querySelectorAll(".blue-link");
        let directors = [];
        directorsElements.forEach((e) => {
            directors.push(e.innerHTML);
        })

        const writersContainer = metaBodyDirection[1];
        const writersElements = writersContainer.querySelectorAll(".blue-link");
        let writers = [];
        writersElements.forEach((e) => {
            writers.push(e.innerHTML);
        })

        const actorsContainer = metaBody.querySelector(".meta-body-actor");
        const actorsElements = actorsContainer.querySelectorAll(".xXx");
        let actors = [];
        actorsElements.forEach((e) => {
            actors.push(e.innerHTML);
        })

        const thumbnail = document.querySelector(".thumbnail-img").src;

        const overviewContainer = document.querySelector("#synopsis-details");
        const overview = overviewContainer.querySelector(".content-txt").innerHTML.trim();


        /*
        *   Technical section datas
        */
        const technicalSection = document.querySelector(".ovw-technical");
        let country;
        let distributor;
        let language;
        let visaNumber;

        Array.from(technicalSection.children).forEach((child, i) => {
            if (i == 0) {
                return
            }

            const key = child.children[0].innerHTML;
            const value = child.children[1];

            if (key == "Nationalité") {
                country = value.children[0].innerHTML;
                country = [country.trim()];
            }
            else if (key == "Nationalités") {
                country = []
                Array.from(value.children).forEach(e => {
                    country.push(e.innerHTML.trim());
                });
            }
            else if (key == "Distributeur") {
                distributor = value.innerHTML;
            }
            else if (key == "Langues") {
                language = value.innerHTML;  // todo(nmj): prepare variables as array
            }
            else if (key == "N° de Visa") {
                visaNumber = value.innerHTML;
            }
            
        });

        // string to array
        language = language.split(",").map(l => l.trim());

        const metaBodyInfo = metaBody.querySelector(".meta-body-info");
        const metaBodyInfoxXx = metaBodyInfo.querySelectorAll(".xXx")
        let date;
        let genres = [];
        let duration = getDuration(metaBodyInfo);
        metaBodyInfoxXx.forEach((e, i) => {
            if (i == 0) {
                date = e.innerHTML.trim()
                return
            }
            genres.push(e.innerHTML)

        });


        data = {
            "title": title,
            "date": date,
            "duration": duration,
            "genres": genres,
            "directors": directors,
            "writers": writers,
            "actors": actors,
            "thumbnail": thumbnail,
            "overview": overview,
            "country": country,
            "distributor": distributor,
            "language": language,
            "visa": visaNumber
        };

        // Send message to the background script because the 
        // content script doesn't have the priviliege to use CROS.
        browser.runtime.sendMessage({
            command: "scrape",
            data: data
        })
    }


    /**
    * Listen for messages from the background script.
    * If url is valid then Call "scrapPage()"
    * Else alert user 
    */
    browser.runtime.onMessage.addListener(async message => {
        if (message.command === "scrap_page") {
            const url = document.location.href
            if (isValidUrl(url)) {
                scrapPage();
            }
            else {
                alert("[FirCinema] [ERROR] Invalid page")
            }
        } 
        else {
            console.log("[FirCinema] [ERROR] Unknown message: " + message.command)
        }
        if(msg.command === "scrape") {
            await sendData(msg.data)
        }
    });
})();
