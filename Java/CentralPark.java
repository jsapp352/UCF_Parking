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

      // try
      // {
      //    readURL(garageDataURL);
      // }
      // catch (Exception e)
      // {
      //
      // }

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

   // static ArrayList<int> readURL(String URLString) throws Exception
   // {
   //   URL garageDataUrl = new URL(URLString);
   //   URLConnection garageData = garageDataUrl.openConnection();
   //   BufferedReader in = new BufferedReader(new InputStreamReader(garageData.getInputStream()));
   //   String inputLine;
   //   while ((inputLine = in.readLine()) != null)
   //       System.out.println(inputLine);
   //   in.close();
   // }

   private static ArrayList<Garage> populateGarageData(String address)
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
         String end = "</td><td id=\"ctl00_MainContent_gvCounts_tccell5_2\" class=\"dxgv\">";
         int startIndex = inputLine.indexOf(start) + start.length();
         int endIndex = inputLine.indexOf(end);
         name = inputLine.substring(startIndex, endIndex);
       }
       else if (inputLine.contains("<td class=\"dxgv\" style=\"border-bottom-width:0px;\">"))
       {
         // Get garage name from UCF website
         String start = "<td class=\"dxgv\" style=\"border-bottom-width:0px;\">";
         String end = "</td><td id=\"ctl00_MainContent_gvCounts_tccell6_2\" class=\"dxgv\" style=\"border-bottom-width:0px;\">";
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
         inputLine = reader.readLine();
         start = "/";
         startIndex = inputLine.indexOf(start) + start.length();
         int capacity = Integer.parseInt(inputLine.substring(startIndex));

         // Add to the list of garages
         garages.add(new Garage(name, available, capacity));
       }
     }

     return garages;
  }

   private static void populateGarageData(ArrayList<Garage> garageList)
   {

   }
}
