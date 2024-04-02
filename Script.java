import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;


public class Script {
    private static final List<String> Books = Arrays.asList("Genesis", "Exodus", "Leviticus", "Numbers", "Deuteronomy", "Joshua", "Judges", "Ruth", "1 Samuel", "2 Samuel",
    "1 Kings", "2 Kings", "1 Chronicles", "2 Chronicles", "Ezra", "Nehemiah", "Esther", "Job", "Psalm", "Proverbs",
    "Ecclesiastes", "Song of Solomon", "Isaiah", "Jeremiah", "Lamentations", "Ezekiel", "Daniel", "Hosea", "Joel",
    "Amos", "Obadiah", "Jonah", "Micah", "Nahum", "Habakkuk", "Zephaniah", "Haggai", "Zechariah", "Malachi", "Matthew",
    "Mark", "Luke", "John", "Acts", "Romans", "1 Corinthians", "2 Corinthians", "Galatians", "Ephesians", "Philippians",
    "Colossians", "1 Thessalonians", "2 Thessalonians", "1 Timothy", "2 Timothy", "Titus", "Philemon", "Hebrews",
    "James", "1 Peter", "2 Peter", "1 John", "2 John", "3 John", "Jude", "Revelation");
    private static final List<String> BooksH = Arrays.asList("בראשית", "שמות", "ויקרא", "במדבר", "דברים", "יהושוע",
            "שופטים", "שמואל א", "שמואל ב", "מלכים א", "מלכים ב", "ישעיה", "ירמיה", "יחזקאל", "הושע", "יואל", "עמוס",
            "עובדיה", "יונה", "מיכה", "נחום", "חבקוק", "צפניה", "חגי", "זכריה", "מלאכי", "תהילים", "משלי", "איוב",
            "שיר השירים", "רות", "איכה", "קהלת", "אסתר", "דניאל", "עזרא", "נחמיה", "דברי הימים א", "דברי הימים ב",
            "מתי", "מרקוס", "לוקס", "יוחנן", "מעשי השליחים", "אל הרומים", "הראשונה אל הקורינתים", "השניה אל הקורינתים",
            "אל הגלטים", "אל האפסים", "אל הפיליפים", "אל הקולוסים", "הראשונה אל התסלונים", "השניה אל התסלונים",
            "הראשונה אל טימותיאוס", "השניה אל טימותיאוס", "אל טיטוס", "אל פילימון", "אל העברים", "אגרת יעקב", "הראשונה לכיפא",
            "השניה לכיפא", "הראשונה ליוחנן", "השניה ליוחנן", "השלישית ליוחנן", "איגרת יהודה", "התגלות");

    public static String reverse(String input) {
        StringBuilder reversed = new StringBuilder();
        for (int i = input.length() - 1; i >= 0; i--) {
            reversed.append(input.charAt(i));
        }
        return reversed.toString();
    }

    public static String decodeUnicode(String encodedStr) {
        StringBuilder sb = new StringBuilder();
        int i = 0;
        while (i < encodedStr.length()) {
            if (encodedStr.charAt(i) == '\\' && i + 1 < encodedStr.length() && encodedStr.charAt(i + 1) == 'u') {
                String hexCode = encodedStr.substring(i + 2, i + 6);
                int unicodeValue = Integer.parseInt(hexCode, 16);
                sb.append((char) unicodeValue);
                i += 6;
            } else {
                sb.append(encodedStr.charAt(i));
                i++;
            }
        }
        return sb.toString();
    }

    public static void main(String[] args) {
        System.out.println("Server is working!");
        ServerSocket serverSocket = null;
        try {
            serverSocket = new ServerSocket(9998);
            while (true) {
                Socket clientSocket = serverSocket.accept(); // Accept incoming connection
                handleClient(clientSocket);
            }
        } catch (IOException e) {
            e.printStackTrace();
        } finally {
            try {
                if (serverSocket != null)
                    serverSocket.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

    private static void handleClient(Socket clientSocket) {
        try {
            PrintWriter out = new PrintWriter(clientSocket.getOutputStream(), true);
            BufferedReader in = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
            String inputLine;
            while ((inputLine = in.readLine()) != null) {
                // Process incoming message
                String rec = decodeUnicode(inputLine);
                String[] parts = rec.split("@");
                String searchTerm = parts[0].replaceAll("^\\s*\"|\"\\s*$", "");
                int numWords = Integer.parseInt(parts[1]);
                int chosenPercent = Integer.parseInt(parts[2].replaceAll("^\\s*\"|\"\\s*$", ""));
                String filePath = parts[3].replaceAll("^\\s*\"|\"\\s*$", "");
                List<String> results;
                if (filePath.equals("bible.txt")) {
                    results = searchInBible(searchTerm, numWords, chosenPercent, Books, filePath);
                }
                else
                    results = searchInBibleH(searchTerm, numWords, chosenPercent, BooksH, filePath);
                for (String result : results) {
                    out.println(result);
                }
                out.println("EOF");
            }
            // Close streams and socket for this client
            out.close();
            in.close();
            clientSocket.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static List<String> searchInBibleH(String searchTerm, int numWords, int chosenPercent,
            List<String> chosenBooks, String filePath) {
        List<String> results = new ArrayList<>();
        double maxPercent = 0;

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath),
                "UTF-8"))) {
            String line;
            boolean flag = false;
            String currentBook = null;

            while ((line = reader.readLine()) != null) {
                if (line.startsWith("$:")) {
                    currentBook = line.split(":")[1].trim();
                    flag = chosenBooks.contains(currentBook);
                } else if (flag) {
                    String verseText = line.trim();
                    List<String> versePartsList = createWordGroups(numWords, verseText);
                    String[] match = bestMatch(searchTerm, versePartsList, currentBook, verseText);
                    double percent = Double.parseDouble(match[1]);
                    if (maxPercent < percent) {
                        maxPercent = percent;
                    }
                    if (percent >= chosenPercent) {
                        String currentVerse = verseText.split("\\s+")[0].split(":")[1];
                        String currentChapter = verseText.split("\\s+")[0].split(":")[0];
                        String words = String.join(" ", verseText.split("\\s+"))
                                .substring(verseText.split("\\s+")[0].length() + 1);
                        results.add(currentBook + "@" + currentChapter + "@" + currentVerse + "@" + words + "@"
                                + match[0] + "@" + percent);
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return results;
    }
    private static List<String> searchInBible(String searchTerm, int numWords, int chosenPercent, List<String> chosenBooks, String filePath) {
        List<String> results = new ArrayList<>();
        double maxPercent = 0;
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath)))) {
            String line;
            boolean flag = false;
            String currentBook = null;

            while ((line = reader.readLine()) != null) {
                if (line.startsWith("T:")) {
                    currentBook = line.split(":")[1].trim();
                    flag = chosenBooks.contains(currentBook);
                } else if (flag) {
                    String verseText = line.trim();
                    List<String> versePartsList = createWordGroups(numWords, verseText);
                    String[] match = bestMatch(searchTerm, versePartsList, currentBook, verseText);
                    double percent = Double.parseDouble(match[1]);
                    if (maxPercent < percent) {
                        maxPercent = percent;
                    }
                    if (percent >= chosenPercent) {
                        String currentVerse = verseText.split("\\s+")[0].split(":")[1];
                        String currentChapter = verseText.split("\\s+")[0].split(":")[0];
                        String words = String.join(" ", verseText.split("\\s+"))
                                .substring(verseText.split("\\s+")[0].length() + 1);
                        results.add(currentBook + "@" + currentChapter + "@" + currentVerse + "@" + words + "@"
                                + match[0] + "@" + percent);
                    }
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return results;
    }
    private static List<String> createWordGroups(int numWords, String text) {
        List<String> wordGroups = new ArrayList<>();
        String[] words = text.split("\\s+");
        for (int i = 0; i <= words.length - numWords; i++) {
            StringBuilder wordGroup = new StringBuilder();
            for (int j = 0; j < numWords; j++) {
                wordGroup.append(words[i + j]).append(" ");
            }
            wordGroups.add(wordGroup.toString().trim());
        }
        return wordGroups;
    }
    public static int getLevenshteinDistance(CharSequence s, CharSequence t) {
        if (s == null || t == null) {
            throw new IllegalArgumentException("Strings must not be null");
        }

        int n = s.length();
        int m = t.length();

        if (n == 0) {
            return m;
        }
        if (m == 0) {
            return n;
        }

        if (n > m) {
            // swap the input strings to consume less memory
            final CharSequence tmp = s;
            s = t;
            t = tmp;
            n = m;
            m = t.length();
        }

        final int[] p = new int[n + 1];
        // indexes into strings s and t
        int i; // iterates through s
        int j; // iterates through t
        int upperleft;
        int upper;

        char jOfT; // jth character of t
        int cost;

        for (i = 0; i <= n; i++) {
            p[i] = i;
        }

        for (j = 1; j <= m; j++) {
            upperleft = p[0];
            jOfT = t.charAt(j - 1);
            p[0] = j;

            for (i = 1; i <= n; i++) {
                upper = p[i];
                cost = s.charAt(i - 1) == jOfT ? 0 : 1;
                // minimum of cell to the left+1, to the top+1, diagonally left and up +cost
                p[i] = Math.min(Math.min(p[i - 1] + 1, p[i] + 1), upperleft + cost);
                upperleft = upper;
            }
        }

        return p[n];
    }
    private static String[] bestMatch(String searchTerm, List<String> list, String currentBook, String currentVerse) {
        String maxMatch = "";
        double maxSimilarity = 0;

        for (String wordGroup : list) {
            int distance = getLevenshteinDistance(wordGroup, searchTerm);
            int maxLength = Math.max(wordGroup.length(), searchTerm.length());
            double similarity = ((double) (maxLength - distance) / maxLength) * 100;

            // System.out.println(reverse(wordGroup.toLowerCase())+", "+similarity);
            if (similarity > maxSimilarity) {
                maxSimilarity = similarity;
                maxMatch = wordGroup;
            }
        }

        return new String[] { maxMatch, String.valueOf(maxSimilarity) };
    }
}

