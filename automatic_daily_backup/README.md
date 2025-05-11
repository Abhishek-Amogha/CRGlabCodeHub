# Automatic Daily Backup | Script & Commands
**S. Abhishek**  

---


Below are the steps to create a simple Bash script to back up your home folder to a specified location on your PC every 24 hours:

## Step 1: Create the Backup Script

1. Open a terminal.
2. Create a new script file, for example, `backup_home.sh`:
3. Add the following content to the script:

   ```bash
   #!/bin/bash

   # Define the source and destination directories
   SOURCE="$HOME"
   DESTINATION="/path/to/backup/location/home_backup"

   # Create the backup directory if it doesn't exist
   mkdir -p "$DESTINATION"

   CURRENT_DATE=$(date +"%Y-%m-%d %H:%M:%S")

   echo "Backup completed on: $CURRENT_DATE" > "$DESTINATION/README.txt"

   # Copy the contents of the home directory to the backup location
   rsync -a --delete "$SOURCE/" "$DESTINATION/"

   echo "Backup completed at $CURRENT_DATE"
   ```

   Replace `/path/to/backup/location/` with the actual path where you want to store the backups.

4. Make the script executable. In the terminal, execute the command:

   ```bash
   chmod +x ~/backup_home.sh
   ```

## Step 2: Schedule the Backup with Cron

1. Open the crontab configuration:

   ```bash
   crontab -e
   ```

2. Add the following line to schedule the script to run every 24 hours (at midnight):

   ```bash
   0 0 * * * DISPLAY=:0 /bin/bash ~/backup_home.sh >> ~/log_home_backup.log 2>&1
   ```

   This line means "run the script at 00:00 (midnight) every day."

3. Save and exit the crontab editor.

## Step 3: Verify the Setup

- You can manually run the script to ensure it works:

  ```bash
  cd
  ./backup_home.sh
  ```

- Check the backup location to confirm that the files are being copied correctly.

## Step 4: Test the Cron Job

To ensure that your cron job works as expected, you can temporarily change the schedule to run every minute for testing purposes:

  ```bash
  * * * * * DISPLAY=:0 /bin/bash ~/backup_home.sh >> ~/log_home_backup.log 2>&1
  ```
	
**After testing, remember to change it back to the desired schedule (e.g., every day at midnight).**
* * *

## Notes

- The `rsync` command is used for efficient file copying. The `-a` option preserves permissions, timestamps, and symbolic links, while `--delete` ensures that files deleted from the source are also removed from the backup.
- You can adjust the timing in the crontab entry if you want to change the frequency of the backups.
- Make sure that the backup location has enough space to store the backups.

### Advantages of using rsync over creating a Zip File:
	
- Incremental Backups: rsync only copies files that have changed since the last backup, making it much faster for subsequent backups. This is especially beneficial for large directories where only a few files change daily.
- Preserves File Attributes: rsync -a preserves file permissions, timestamps, and other attributes, ensuring that the backup is a true mirror of the source.
- Easy Restoration: You can easily restore individual files or directories from the backup without needing to extract an archive.
- Efficient Use of Space: The --delete option ensures that the backup location mirrors the source, removing files that no longer exist in the source, which helps manage disk space.
