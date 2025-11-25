import java.awt.Graphics;
import java.awt.image.*;
import java.io.*;
import java.net.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.concurrent.atomic.AtomicInteger;
import javax.imageio.ImageIO;

public class ImagePipeline {

    static class ImageTask {
        String url;
        BufferedImage image;
        int index;
        boolean isPoisonPill;

        ImageTask(String url) {
            this.url = url;
            this.isPoisonPill = false;
        }

        ImageTask(BufferedImage image, int index) {
            this.image = image;
            this.index = index;
            this.isPoisonPill = false;
        }

        static ImageTask poisonPill() {
            ImageTask task = new ImageTask((BufferedImage) null, -1);
            task.isPoisonPill = true;
            return task;
        }
    }

    public static void main(String[] args) throws Exception {

        Files.createDirectories(Path.of("out"));

        var executor = Executors.newVirtualThreadPerTaskExecutor();

        // Queues for pipeline stages
        BlockingQueue<String> urlQueue = new LinkedBlockingQueue<>();
        BlockingQueue<ImageTask> downloadQueue = new LinkedBlockingQueue<>();
        BlockingQueue<ImageTask> convertQueue = new LinkedBlockingQueue<>();
        BlockingQueue<ImageTask> saveQueue = new LinkedBlockingQueue<>();

        // Feeder: read URLs from file and enqueue them
        executor.submit(() -> {
            try {
                List<String> urls = readUrls("images.csv");
                for (String url : urls) {
                    urlQueue.put(url);
                }
                // Signal end of URLs
                for (int i = 0; i < 4; i++) {
                    urlQueue.put("END");
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        });

        // Downloaders: download images from URLs
        int numDownloaders = 4;
        AtomicInteger imageIndex = new AtomicInteger(0);
        for (int i = 0; i < numDownloaders; i++) {
            executor.submit(() -> {
                try {
                    while (true) {
                        String url = urlQueue.take();
                        if (url.equals("END")) {
                            urlQueue.put("END");
                            downloadQueue.put(ImageTask.poisonPill());
                            break;
                        }
                        BufferedImage image = downloadImage(url);
                        int index = imageIndex.getAndIncrement();
                        downloadQueue.put(new ImageTask(image, index));
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
        }

        // Converters: convert images to grayscale
        int numConverters = 4;
        for (int i = 0; i < numConverters; i++) {
            executor.submit(() -> {
                try {
                    while (true) {
                        ImageTask task = downloadQueue.take();
                        if (task.isPoisonPill) {
                            convertQueue.put(ImageTask.poisonPill());
                            break;
                        }
                        BufferedImage gray = toGrayscale(task.image);
                        convertQueue.put(new ImageTask(gray, task.index));
                    }
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
        }

        // Saver: write grayscale images to disk
        executor.submit(() -> {
            try {
                int endCount = 0;
                while (endCount < numConverters) {
                    ImageTask task = convertQueue.take();
                    if (task.isPoisonPill) {
                        endCount++;
                        continue;
                    }
                    String filename = "out/image_" + task.index + ".png";
                    saveImage(task.image, filename);
                    System.out.println("Saved: " + filename);
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        });

        executor.shutdown();
        executor.awaitTermination(2, TimeUnit.MINUTES);
        System.out.println("Pipeline completed!");
    }

    static List<String> readUrls(String filename) throws IOException {
        return Files.readAllLines(Path.of(filename));
    }

    static BufferedImage downloadImage(String url) throws IOException {
        return ImageIO.read(URI.create(url).toURL());
    }

    static BufferedImage toGrayscale(BufferedImage image) {
        BufferedImage gray = new BufferedImage(image.getWidth(), image.getHeight(), BufferedImage.TYPE_BYTE_GRAY);
        Graphics graphics = gray.getGraphics();
        graphics.drawImage(image, 0, 0, null);
        graphics.dispose();
        return gray;
    }

    static void saveImage(BufferedImage image, String filename) throws IOException {
        ImageIO.write(image, "png", new File(filename));
    }
}
