import { readFile } from 'node:fs/promises';

async function processBook(urlString) {
    try {
        const response = await fetch(urlString);
        const text = await response.text();
        const words = text.toLowerCase().split(/\W+/);
        const counts = new Map();
        for (const word of words) {
            if (word) {
                counts.set(word, (counts.get(word) || 0) + 1);
            }
        }
        return counts;
    } catch (e) {
        console.error('Failed to process book:', urlString, e.message);
        return new Map();
    }
}

async function main() {
    const urls = (await readFile('books.csv', 'utf8')).trim().split('\n').filter(line => line.trim());

    const promises = urls.map(url => processBook(url));
    const bookCounts = await Promise.all(promises);

    const globalCounts = new Map();
    for (const counts of bookCounts) {
        for (const [word, count] of counts) {
            globalCounts.set(word, (globalCounts.get(word) || 0) + count);
        }
    }

    const sortedWords = Array.from(globalCounts.entries())
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10);

    console.log('\nTop 10 most frequent words:');
    for (let i = 0; i < sortedWords.length; i++) {
        const [word, count] = sortedWords[i];
        console.log(`${i + 1}. ${word}: ${count}`);
    }
}

await main();

