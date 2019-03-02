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
        ArrayList<Garage> garageList = populateGarageData(garageDataURL);
      }
      catch (Exception e)
      {
        System.out.println("Could not webscrape UCF Parking Data!");
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

   private static ArrayList<Garage> populateGarageData(String address) throws Exception
   {
     ArrayList<Garage> garages = new ArrayList<>();
     String inputLine;
     String name = "Garage Something";
     URL url = new URL(address);
     BufferedReader reader = new BufferedReader(new InputStreamReader(url.openStream(), "UTF-8"));

     while ((inputLine = reader.readLine()) != null)
     {

       if (inputLine.contains("<td class=\"dxgv\">"))
       {
         // Get available capacity from UCF website
         String start = "<td class=\"dxgv\">";
         String end = "</td>";
         int startIndex = inputLine.indexOf(start) + start.length();
         int endIndex = inputLine.indexOf(end);
         name = inputLine.substring(startIndex, endIndex);
       }
       else if (inputLine.contains("<td class=\"dxgv\" style=\"border-bottom-width:0px;\">"))
       {
         // Get garage name from UCF website
         String start = "<td class=\"dxgv\" style=\"border-bottom-width:0px;\">";
         String end = "</td>";
         int startIndex = inputLine.indexOf(start) + start.length();
         int endIndex = inputLine.indexOf(end);
         name = inputLine.substring(startIndex, endIndex);
       }
       else if (inputLine.contains("<strong>") == true)
       {
         // Get available capacity from UCF website
         String start = "<strong>";
         String end = "</strong>";
         int startIndex = inputLine.indexOf(start) + start.length();
         int endIndex = inputLine.indexOf(end);
         int available = Integer.parseInt(inputLine.substring(startIndex, endIndex));

         // Get total capacity from UCF website
         start = "/";
         startIndex = inputLine.lastIndexOf(start) + start.length();
         int capacity = Integer.parseInt(inputLine.substring(startIndex));

         // Add to the list of garages
         garages.add(new Garage(name, available, capacity));
       }
     }

     return garages;
  }
}
