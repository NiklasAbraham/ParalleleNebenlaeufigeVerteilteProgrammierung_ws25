import { readFile, mkdir, writeFile } from 'node:fs/promises';
import sharp from 'sharp';

await mkdir('out', { recursive: true });

async function readUrls(filename) {
    return (await readFile(filename, 'utf8')).trim().split('\n').filter(line => line.trim());
}

async function downloadImage(url) {
    try {
        const response = await fetch(url);
        const buffer = Buffer.from(await response.arrayBuffer());
        return buffer;
    } catch (e) {
        console.error('Failed to download:', url, e.message);
        return null;
    }
}

async function toGrayscale(imageBuffer) {
    return await sharp(imageBuffer).grayscale().toBuffer();
}

async function saveImage(buffer, filename) {
    await writeFile(filename, buffer);
}

async function* urlGenerator(filename) {
    const urls = await readUrls(filename);
    for (const url of urls) {
        yield url;
    }
}

async function* downloadGenerator(urlIterator, concurrency = 4) {
    const downloadQueue = [];
    let index = 0;

    const urlPromises = [];
    for await (const url of urlIterator) {
        const currentIndex = index++;
        const promise = downloadImage(url).then(buffer => ({
            buffer,
            index: currentIndex
        }));
        downloadQueue.push(promise);

        if (downloadQueue.length >= concurrency) {
            const result = await Promise.race(
                downloadQueue.map((p, i) => p.then(r => ({ result: r, idx: i })))
            );
            yield result.result;
            downloadQueue.splice(result.idx, 1);
        }
    }

    while (downloadQueue.length > 0) {
        const result = await Promise.race(
            downloadQueue.map((p, i) => p.then(r => ({ result: r, idx: i })))
        );
        yield result.result;
        downloadQueue.splice(result.idx, 1);
    }
}

async function* convertGenerator(imageIterator, concurrency = 4) {
    const convertQueue = [];

    for await (const { buffer, index } of imageIterator) {
        if (!buffer) continue;
        const promise = toGrayscale(buffer).then(grayBuffer => ({
            buffer: grayBuffer,
            index
        }));
        convertQueue.push(promise);

        if (convertQueue.length >= concurrency) {
            const result = await Promise.race(
                convertQueue.map((p, i) => p.then(r => ({ result: r, idx: i })))
            );
            yield result.result;
            convertQueue.splice(result.idx, 1);
        }
    }

    while (convertQueue.length > 0) {
        const result = await Promise.race(
            convertQueue.map((p, i) => p.then(r => ({ result: r, idx: i })))
        );
        yield result.result;
        convertQueue.splice(result.idx, 1);
    }
}

async function saveGenerator(imageIterator) {
    for await (const { buffer, index } of imageIterator) {
        const filename = `out/image_${index}.png`;
        await saveImage(buffer, filename);
        console.log(`Saved: ${filename}`);
    }
}

async function main() {
    const urlIter = urlGenerator('images.csv');
    const downloadIter = downloadGenerator(urlIter, 4);
    const convertIter = convertGenerator(downloadIter, 4);
    await saveGenerator(convertIter);
    console.log('Pipeline completed!');
}

await main();
