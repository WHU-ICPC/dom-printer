/**
 * @author 13090
 * @version 1.0
 * @description: TODO
 * @date 2023/4/25 14:59
 */

import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.web.bind.annotation.*;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.nio.file.StandardCopyOption;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

@RestController
public class FileController {
    private static final String BASE_DIR = "{basedir}";
    private static final String NEW_DIR = BASE_DIR + "/new";
    private static final String OLD_DIR = BASE_DIR + "/old";
    private final Map<String, Long> processedFiles = new ConcurrentHashMap<>();

    @GetMapping("/api/print")
    public ResponseEntity<Map<String, String>> getFileInfo() {
        File newDir = new File(NEW_DIR);
        File[] files = newDir.listFiles((dir, name) -> name.endsWith(".txt"));

        if (files == null || files.length == 0) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
        }

        for (File file : files) {
            String randomShit = file.getName().substring(0, file.getName().length() - 4);
            if (!processedFiles.containsKey(randomShit)) {
                File datFile = new File(NEW_DIR, randomShit + ".dat");
                try {
                    String info = Base64.getEncoder().encodeToString(Files.readAllBytes(file.toPath()));
                    String data = Base64.getEncoder().encodeToString(Files.readAllBytes(datFile.toPath()));

                    Map<String, String> response = new HashMap<>();
                    response.put("id", randomShit);
                    response.put("info", info);
                    response.put("data", data);

                    processedFiles.put(randomShit, System.currentTimeMillis());
                    return ResponseEntity.ok(response);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }

        return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @DeleteMapping("/api/print/{randomShit}")
    public ResponseEntity<?> deleteFile(@PathVariable String randomShit) {
        if (processedFiles.containsKey(randomShit)) {
            File txtFile = new File(NEW_DIR, randomShit + ".txt");
            File datFile = new File(NEW_DIR, randomShit + ".dat");
            try {
                Files.move(txtFile.toPath(), Paths.get(OLD_DIR, txtFile.getName()), StandardCopyOption.REPLACE_EXISTING);
                Files.move(datFile.toPath(), Paths.get(OLD_DIR,
                        datFile.getName()), StandardCopyOption.REPLACE_EXISTING);
                processedFiles.remove(randomShit);
                return ResponseEntity.ok().build();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        return ResponseEntity.status(HttpStatus.NOT_FOUND).build();
    }

    @Scheduled(fixedRate = 30000)
    public void cleanProcessedFiles() {
        long currentTime = System.currentTimeMillis();
        processedFiles.entrySet().removeIf(entry -> currentTime - entry.getValue() > 30000);
    }

}
