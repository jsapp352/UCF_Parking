import java.lang.*;
import java.util.*;
import java.io.*;

public class CentralPark
{
   public static void main(String [] args)
   {
      File f = new File("googlemap_key.txt");

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
}
