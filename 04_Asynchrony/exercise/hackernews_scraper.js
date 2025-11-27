async function fetchTopStories() {
    const url = `https://hacker-news.firebaseio.com/v0/topstories.json?limitToFirst=30&orderBy="$key"`;
    try {
        const response = await fetch(url);
        const storyIds = await response.json();
        return storyIds;
    } catch (e) {
        console.error('Failed to fetch top stories:', e.message);
        return [];
    }
}

async function fetchItem(id) {
    const url = `https://hacker-news.firebaseio.com/v0/item/${id}.json`;
    try {
        const response = await fetch(url);
        const item = await response.json();
        return item;
    } catch (e) {
        console.error('Failed to fetch item:', id, e.message);
        return null;
    }
}



async function main() {
    const storyIds = await fetchTopStories();
    console.log('Story IDs:', storyIds);
    
    // Fetch the actual story objects
    const stories = await Promise.all(storyIds.map(id => fetchItem(id)));
    console.log('Stories:', stories);

    // from there each of the stories has a id, each storys id has a kids field, which is first a comment, and then kids again a reply
    // so we need to fetch the comment and then the reply
    // then it needs to be mapped to a new object with the story, comment and reply
    const storiesWithCommentsAndReplies = await Promise.all(stories.map(async (story) => {
        if (!story || !story.kids || story.kids.length === 0) {
            return { story, comment: null, reply: null };
        }
        const comment = await fetchItem(story.kids[0]);
        if (!comment || !comment.kids || comment.kids.length === 0) {
            return { story, comment, reply: null };
        }
        const reply = await fetchItem(comment.kids[0]);
        return { story, comment, reply };   
    }));
    console.log(storiesWithCommentsAndReplies);
}



await main();