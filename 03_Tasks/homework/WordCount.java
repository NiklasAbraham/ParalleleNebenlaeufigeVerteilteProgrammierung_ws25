import java.net.*;
import java.nio.file.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.stream.Collectors;

public class WordCount {

    public static void main(String[] args) throws Exception {

        List<String> urls = Files.readAllLines(Path.of("books.csv"));

        ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();

        // Process books in parallel
        List<Future<HashMap<String, Integer>>> futures = new ArrayList<>();
        for (String url : urls) {
            Future<HashMap<String, Integer>> future = executor.submit(() -> processBook(url));
            futures.add(future);
        }

        // Merge all hashmaps to get global word count
        HashMap<String, Integer> globalCounts = new HashMap<>();
        for (Future<HashMap<String, Integer>> future : futures) {
            HashMap<String, Integer> bookCounts = future.get();
            for (Map.Entry<String, Integer> entry : bookCounts.entrySet()) {
                globalCounts.merge(entry.getKey(), entry.getValue(), Integer::sum);
            }
        }

        // Output the 10 most frequent words
        List<Map.Entry<String, Integer>> sortedWords = globalCounts.entrySet().stream()
            .sorted(Map.Entry.<String, Integer>comparingByValue().reversed())
            .limit(10)
            .collect(Collectors.toList());

        System.out.println("\nTop 10 most frequent words:");
        for (int i = 0; i < sortedWords.size(); i++) {
            Map.Entry<String, Integer> entry = sortedWords.get(i);
            System.out.println((i + 1) + ". " + entry.getKey() + ": " + entry.getValue());
        }

        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.MINUTES);
    }

    static HashMap<String, Integer> processBook(String urlString) throws Exception {
        URL url = URI.create(urlString).toURL();
        String text = new String(url.openStream().readAllBytes());
        String[] words = text.toLowerCase().split("\\W+");
        HashMap<String, Integer> counts = new HashMap<>();
        for (String word : words) {
            if (!word.isEmpty()) {
                counts.merge(word, 1, Integer::sum);
            }
        }
        return counts;
    }
}
