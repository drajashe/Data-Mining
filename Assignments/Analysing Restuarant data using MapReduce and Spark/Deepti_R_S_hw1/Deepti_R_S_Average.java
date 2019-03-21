import java.io.IOException;
import java.util.StringTokenizer;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.util.GenericOptionsParser;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;


public class Deepti_R_S_Average{

  public static class Event_Mapper
       extends Mapper<LongWritable , Text, Text, Text>{

    private Text event = new Text();
    private Text add_one = new Text();


    public void map(LongWritable  Key, Text Value, Context context
                    ) throws IOException, InterruptedException {

        try {
            if (Key.get() == 0 && Value.toString().contains("id") ) return;

            else {
                // For rest of data it goes here

                String input_data = Value.toString();
                String[] input_data_split = input_data.split(",",-1);
                String events_string = input_data_split[3];

                String page_count_string = input_data_split[18];
                page_count_string.trim();

                events_string = events_string.replaceAll("[^\\p{L}\\p{Nd}]+", " ").replace("^"," ").replaceAll("[\\p{Cntrl}&&[^\r\n\t]]", "").replaceAll("\\p{C}", " ");
                events_string=events_string.toLowerCase().trim();


	            //handle the empty events

	            if(events_string.equals(null) || (events_string.equals(""))) return;

                	add_one.set(page_count_string + "," + "1");

		        event.set(events_string);;


		        context.write(event,add_one);
                }

        } catch (Exception e)
        {
                e.printStackTrace();

         }

    }
  }


  public static class Avg_Reducer
       extends Reducer<Text,Text,Text,Text> {

    Text out_reducer = new Text();
   
    public void reduce(Text Key, Iterable<Text> values,
                       Context context
                       ) throws IOException, InterruptedException {
        int sum = 0;
        int count =0;
        float average=0;
        int split_value_cnt=0;
        int  split_value_pg_cnt=0;
        
        
        

        
        for (Text val : values) 
        {
                String[] temp = val.toString().split(",");
                split_value_cnt = Integer.parseInt(temp[1]);
                split_value_pg_cnt = Integer.parseInt(temp[0]);
                
                
                count+=split_value_cnt;
                sum+=split_value_pg_cnt;
                average= sum/count;

        }

        
        
        String total_avg = String.valueOf(average)
                + " " + String.valueOf(count);


        out_reducer.set(total_avg);
        
        context.write(Key,out_reducer);
    }
  }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    String[] otherArgs = new GenericOptionsParser(conf, args).getRemainingArgs();
    if (otherArgs.length < 2) {
      System.err.println("Usage: wordcount <in> [<in>...] <out>");
      System.exit(2);
    }
    
    Job job = Job.getInstance(conf, "event_avg");
    job.setJarByClass(Deepti_R_S_Average.class);
    job.setMapOutputKeyClass(Text.class);
    job.setMapOutputValueClass(Text.class);
    job.setMapperClass(Event_Mapper.class);
    job.setReducerClass(Avg_Reducer.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(Text.class);
    for (int i = 0; i < otherArgs.length - 1; ++i) {
      FileInputFormat.addInputPath(job, new Path(otherArgs[i]));
    }
    FileOutputFormat.setOutputPath(job,
      new Path(otherArgs[otherArgs.length - 1]));
    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}


