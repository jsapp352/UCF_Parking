import java.lang.*;
import java.net.*;
import java.util.*;
import java.io.*;

public class CentralPark
{
   public static void main(String [] args)
   {
      String garageDataURL = "http://secure.parking.ucf.edu/GarageCount/";
      String API_key_filename = "googlemap_key.txt";

      try
      {
         readURL(garageDataURL);
      }
      catch (Exception e)
      {

      }

      File f = new File(API_key_filename);

      try
      {
         Scanner key_scan = new Scanner(f);
         String API_key = key_scan.next();
         System.out.println(API_key);
      }
      catch (FileNotFoundException e)
      {
         System.out.println("Could not open API key file.");
      }



   }

   static void readURL(String URLString) throws Exception
   {
     URL garageDataUrl = new URL(URLString);
     URLConnection garageData = garageDataUrl.openConnection();
     BufferedReader in = new BufferedReader(new InputStreamReader(garageData.getInputStream()));
     String inputLine;
     while ((inputLine = in.readLine()) != null)
         System.out.println(inputLine);
     in.close();
   }
}
