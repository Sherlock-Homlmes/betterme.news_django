const choosen_topic = document.getElementById("topic");
const search_input = document.getElementById("search-input");
const search_dropdown = document.getElementById("dropdownSearch");
const client = new MeiliSearch({ host: 'http://localhost:7700', apiKey: 'masterKey' });
const index = client.index('news');
var lim = 10;
let topic_type = {};

//topic converter
$.ajax({
    type: 'GET',
    url: '/topic-type/',
    success: function (request) {
        topic_type = request;
    },
    error: function (error) {
        console.log("can't get topic_type");
    }
})

//search engine
async function search_news(name, tag) {
    if (tag == "") {
        var results = await index.search(name, {
            limit: lim,
            attributesToHighlight: ["*"],
        });
    }
    else {
        console.log(name, tag)
        var results = await index.search(name,
            {
                filter: ["tags = " + tag],
                limit: lim,
                attributesToHighlight: ["*"],
                // sort: ['id:desc'],
            });
    }
    //console.log(results);
    return results;
}

function instant_search() {
    (async () => {
        if (search_input.value == "") {
            search_dropdown.innerHTML = ``;
        }
        else {
            const results = await search_news(search_input.value, topic_type[choosen_topic.innerText])
                .then(function (result) { return result.hits });
            // console.log(results);
            if (results.length > 0) {

                search_dropdown.innerHTML = `<ul id="news-block" class="py-1 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownSearchButton"></ul>`;
                for (let hit = 1; hit < results.length; hit++) {
                    document.getElementById('news-block').innerHTML += `<li>
                        <a href="${results[hit].name}" class="block py-2 px-4 hover:bg-gray-100 dark:hover:bg-gray-600 dark:hover:text-white">
                        <img src="${results[hit].thumbnail_link}">
                        <strong>${results[hit].title}</strong>
                        </a>
                    </li>`;
                };

            }
            else {
                search_dropdown.innerHTML = `
                <ul class="py-1 text-sm text-gray-700 dark:text-gray-200" aria-labelledby="dropdownSearchButton">
                    <li style="display:flex;align-items:center;">
                    <i>Không thấy kết quả</i>
                    </li>
                </ul>
                `;
            }
        }

    })()

}

$('#choose-topic li').on('click', function () {
    choosen_topic.innerHTML = $(this).text();
    //console.log(search_input.value)
    if (search_input.value != "") {
        instant_search();
    }

});

$("#search-input").keyup(function () {
    instant_search();
});

$("#search-input").keydown(function () {
    instant_search();
});