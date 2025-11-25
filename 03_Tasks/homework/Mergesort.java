import java.util.Arrays;
import java.util.Random;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.concurrent.Future;
import java.util.concurrent.ExecutionException;

class Mergesort {
    public static int[] mergesort(int[] array, ExecutorService executor)
        throws InterruptedException, ExecutionException {

        if (array.length <= 1) {
            return array;
        }

        int mid = array.length / 2;
        int[] left = Arrays.copyOfRange(array, 0, mid);
        int[] right = Arrays.copyOfRange(array, mid, array.length);

        Future<int[]> leftFuture = executor.submit(() -> mergesort(left, executor));
        Future<int[]> rightFuture = executor.submit(() -> mergesort(right, executor));

        int[] sortedLeft = leftFuture.get();
        int[] sortedRight = rightFuture.get();

        return merge(sortedLeft, sortedRight);
    }

    public static String[] mergesort(String[] array, ExecutorService executor)
        throws InterruptedException, ExecutionException {

        if (array.length <= 1) {
            return array;
        }

        int mid = array.length / 2;
        String[] left = Arrays.copyOfRange(array, 0, mid);
        String[] right = Arrays.copyOfRange(array, mid, array.length);

        Future<String[]> leftFuture = executor.submit(() -> mergesort(left, executor));
        Future<String[]> rightFuture = executor.submit(() -> mergesort(right, executor));

        String[] sortedLeft = leftFuture.get();
        String[] sortedRight = rightFuture.get();

        return merge(sortedLeft, sortedRight);
    }

    private static int[] merge(int[] left, int[] right) {
        int[] result = new int[left.length + right.length];
        int i = 0, j = 0, k = 0;

        while (i < left.length && j < right.length) {
            if (left[i] <= right[j]) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }

        while (i < left.length) {
            result[k++] = left[i++];
        }

        while (j < right.length) {
            result[k++] = right[j++];
        }

        return result;
    }

    private static String[] merge(String[] left, String[] right) {
        String[] result = new String[left.length + right.length];
        int i = 0, j = 0, k = 0;

        while (i < left.length && j < right.length) {
            if (left[i].compareTo(right[j]) <= 0) {
                result[k++] = left[i++];
            } else {
                result[k++] = right[j++];
            }
        }

        while (i < left.length) {
            result[k++] = left[i++];
        }

        while (j < right.length) {
            result[k++] = right[j++];
        }

        return result;
    }

    public static int[] randomIntArray(int size) {
        int[] array = new int[size];
        Random random = new Random();

        for (int i = 0; i < array.length; i++) {
            array[i] = random.nextInt(1000000);
        }
        return array;
    }

    public static String[] randomStringArray(int size) {
        String[] array = new String[size];
        Random random = new Random();
        String chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for (int i = 0; i < array.length; i++) {
            int length = random.nextInt(10) + 1;
            StringBuilder sb = new StringBuilder();
            for (int j = 0; j < length; j++) {
                sb.append(chars.charAt(random.nextInt(chars.length())));
            }
            array[i] = sb.toString();
        }
        return array;
    }

    public static void benchmarkInts(int size) throws Exception {
        System.out.println("\n=== Benchmarking Integer Arrays (size: " + size + ") ===");
        
        ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
        
        int[] array1 = randomIntArray(size);
        int[] array2 = Arrays.copyOf(array1, array1.length);
        int[] array3 = Arrays.copyOf(array1, array1.length);

        // Parallel mergesort
        long startTime = System.nanoTime();
        int[] sorted1 = mergesort(array1, executor);
        long endTime = System.nanoTime();
        double duration1 = (endTime - startTime) / 1_000_000.0;
        System.out.println("Parallel Mergesort: " + duration1 + " ms");

        // Arrays.sort
        startTime = System.nanoTime();
        Arrays.sort(array2);
        endTime = System.nanoTime();
        double duration2 = (endTime - startTime) / 1_000_000.0;
        System.out.println("Arrays.sort: " + duration2 + " ms");

        // Arrays.parallelSort
        startTime = System.nanoTime();
        Arrays.parallelSort(array3);
        endTime = System.nanoTime();
        double duration3 = (endTime - startTime) / 1_000_000.0;
        System.out.println("Arrays.parallelSort: " + duration3 + " ms");

        executor.shutdown();
    }

    public static void benchmarkStrings(int size) throws Exception {
        System.out.println("\n=== Benchmarking String Arrays (size: " + size + ") ===");
        
        ExecutorService executor = Executors.newVirtualThreadPerTaskExecutor();
        
        String[] array1 = randomStringArray(size);
        String[] array2 = Arrays.copyOf(array1, array1.length);
        String[] array3 = Arrays.copyOf(array1, array1.length);

        // Parallel mergesort
        long startTime = System.nanoTime();
        String[] sorted1 = mergesort(array1, executor);
        long endTime = System.nanoTime();
        double duration1 = (endTime - startTime) / 1_000_000.0;
        System.out.println("Parallel Mergesort: " + duration1 + " ms");

        // Arrays.sort
        startTime = System.nanoTime();
        Arrays.sort(array2);
        endTime = System.nanoTime();
        double duration2 = (endTime - startTime) / 1_000_000.0;
        System.out.println("Arrays.sort: " + duration2 + " ms");

        // Arrays.parallelSort
        startTime = System.nanoTime();
        Arrays.parallelSort(array3);
        endTime = System.nanoTime();
        double duration3 = (endTime - startTime) / 1_000_000.0;
        System.out.println("Arrays.parallelSort: " + duration3 + " ms");

        executor.shutdown();
    }

    public static void main(String[] args) throws Exception {
        int[] sizes = {10000, 100000, 1000000, 10000000};

        for (int size : sizes) {
            benchmarkInts(size);
        }

        for (int size : sizes) {
            benchmarkStrings(size);
        }
    }
}

