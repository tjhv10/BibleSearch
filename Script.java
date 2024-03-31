import java.io.*;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.apache.commons.lang3.StringUtils;
import java.net.*;



    


public class Script {

    private static final List<String> BooksH = Arrays.asList(
    "בראשית", "שמות", "ויקרא", "במדבר", "דברים", "יהושוע", "שופטים", "שמואל א", "שמואל ב", "מלכים א", "מלכים ב", "ישעיה",
    "ירמיה", "יחזקאל", "הושע", "יואל", "עמוס", "עובדיה", "יונה", "מיכה", "נחום", "חבקוק", "צפניה", "חגי", "זכריה",
    "מלאכי", "תהילים", "משלי", "איוב", "שיר השירים", "רות", "איכה", "קהלת", "אסתר", "דניאל", "עזרא", "נחמיה",
    "דברי הימים א", "דברי הימים ב", "מתי", "מרקוס", "לוקס", "יוחנן", "מעשי השליחים", "אל הרומים", "הראשונה אל הקורינתים",
    "השניה אל הקורינתים", "אל הגלטים", "אל האפסים", "אל הפיליפים", "אל הקולוסים", "הראשונה אל התסלוניקים",
    "השניה אל התסלוניקים", "הראשונה אל טימותיאוס", "השניה אל טימותיאוס", "אל טיטוס", "אל פילימון", "אל העברים", "אגרת יעקב",
    "הראשונה לכיפא", "השניה לכיפא", "הראשונה ליוחנן", "השניה ליוחנן", "השלישית ליוחנן", "איגרת יהודה", "התגלות"
);
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
    public static void main(String[] args) throws IOException {
        ServerSocket serverSocket = new ServerSocket(9998);
    
        try {
            while (true) {
                Socket clientSocket = serverSocket.accept(); // Accept incoming connection
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
                    List<String> chosenBooks = BooksH;
                    String filePath = "BibleH.txt";
                    List<String> results = searchInBibleH(searchTerm, numWords, chosenPercent, chosenBooks, filePath);
                    for (String result : results) {
                        System.out.println(reverse(result));
                    }
                }
    
                // Close streams and socket for this client
                out.close();
                in.close();
                clientSocket.close();
            }
        } catch (IOException e) {
            e.printStackTrace(); // Print the stack trace for debugging
        } finally {
            // Close the server socket
            serverSocket.close();
        }
    }
    

    

    private static List<String> searchInBibleH(String searchTerm, int numWords, int chosenPercent,
                                               List<String> chosenBooks, String filePath) {
        List<String> results = new ArrayList<>();
        double maxPercent = 0;

        try (BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(filePath), "UTF-8"))) {
            String line;
            boolean flag = false;
            String currentBook = null;
            
            while ((line = reader.readLine()) != null) {
                if (line.startsWith("$:")) {
                    currentBook = line.split(":")[1].trim();
                    flag = chosenBooks.contains(currentBook);
                } else if (flag) {
                    String verseText = line.trim();
                    // System.out.println(reverse(verseText));
                    List<String> versePartsList = createWordGroups(numWords, verseText);
                    String[] match = bestMatch(searchTerm, versePartsList, currentBook, verseText);
                    double percent = Double.parseDouble(match[1]);
                    if (maxPercent < percent) {
                        maxPercent = percent;
                    }
                    if (percent >= chosenPercent) {
                        String currentVerse = verseText.split("\\s+")[0].split(":")[1];
                        String currentChapter = verseText.split("\\s+")[0].split(":")[0];
                        String words = String.join(" ", verseText.split("\\s+")).substring(verseText.split("\\s+")[0].length() + 1);
                        results.add(currentBook + " " + currentChapter + " " + currentVerse + " " + words + " " + match[0] + " " + percent);
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

    private static String[] bestMatch(String searchTerm, List<String> list, String currentBook, String currentVerse) {
        String maxMatch = "";
        double maxSimilarity = 0;

        for (String wordGroup : list) {
            @SuppressWarnings("deprecation")
            int distance = StringUtils.getLevenshteinDistance(wordGroup, searchTerm);
            int maxLength = Math.max(wordGroup.length(), searchTerm.length());
            double similarity = ((double) (maxLength - distance) / maxLength) * 100;

            // System.out.println(reverse(wordGroup.toLowerCase())+", "+similarity);
            if (similarity > maxSimilarity) {
                maxSimilarity = similarity;
                maxMatch = wordGroup;
            }
        }

        return new String[]{maxMatch, String.valueOf(maxSimilarity)};
    }

    
}
