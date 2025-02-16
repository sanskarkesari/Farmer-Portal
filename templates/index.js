// Sample news data (can be replaced with an API call)
const newsData = [
    { title: "New subsidy announced for organic farming.", link: "#" },
    { title: "Weather alert: Heavy rainfall expected in the next week.", link: "#" },
    { title: "Government launches new loan scheme for small farmers.", link: "#" },
    { title: "Market prices for wheat rise by 10%.", link: "#" },
];

// Function to dynamically add news items to the news column
function loadNews() {
    const newsList = document.getElementById("news-list");

    newsData.forEach((news) => {
        const listItem = document.createElement("li");
        const link = document.createElement("a");
        link.href = news.link;
        link.textContent = news.title;
        listItem.appendChild(link);
        newsList.appendChild(listItem);
    });
}

// Load news when the page loads
window.onload = loadNews;