CREATE DATABASE music_database;
USE music_database;
CREATE TABLE MusicFile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    file_name VARCHAR(255),
    file_path VARCHAR(255)
);

INSERT INTO MusicFile (file_name, file_path)
VALUES 
  ('Ae-Dil-Hai-Mushkil.mp3','C:\\Users\\anike\\AppData\\Local\\Programs\\Python\\Python312\\Python project Music Player\\Music Files\\Ae-Dil-Hai-Mushkil-Title-Track_320(PagalWorldl).mp3'),
  ('Jo-Tu-Mera-Humdard-Hai.mp3','C:\\Users\\anike\\AppData\\Local\\Programs\\Python\\Python312\\Python project Music Player\\Music Files\\Jo-Tu-Mera-Humdard-Hai_320(PagalWorldl).mp3'),
  ('Zara-Zara.mp3','C:\\Users\\anike\\AppData\\Local\\Programs\\Python\\Python312\\Python project Music Player\\Music Files\\Zara-Zara_320(PagalWorldl).mp3'),
  ('Aigiri-Nandini.mp3','C:\\Users\\anike\\AppData\\Local\\Programs\\Python\\Python312\\Python project Music Player\\Music Files\\Aigiri-Nandini_320(PagalWorldl).mp3'),
  ('Sach-Keh-Raha-Hai-Deewana.mp3','C:\\Users\\anike\\AppData\\Local\\Programs\\Python\\Python312\\Python project Music Player\\Music Files\\Sach-Keh-Raha-Hai-Deewana-(Cover-Version)(PaglaSongs).mp3');
       
select * from music_file;