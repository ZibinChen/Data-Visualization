package edu.gatech.cse6242;
import java.io.IOException;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Q1 {
    public static class TokenMapper
    extends Mapper<Object, Text, IntWritable, IntWritable>{
        public void map(Object key, Text value, Context context
                        ) throws IOException, InterruptedException {
            String line = value.toString();
            if (line.contains("\t")) {
                String[] columns = line.split("\t");
                IntWritable src = new IntWritable(Integer.parseInt(columns[0]));
                IntWritable weight = new IntWritable(Integer.parseInt(columns[2]));
                context.write(src, weight);
            }
        }
    }
    
    public static class IntMaximumReducer
    extends Reducer<IntWritable,IntWritable,IntWritable,IntWritable> {
        private IntWritable result = new IntWritable();
        public void reduce(IntWritable key, Iterable<IntWritable> values,
                           Context context
                           ) throws IOException, InterruptedException {
            int max = -1;
            for (IntWritable val : values) {
                if (val.get() > max) {
                    max = val.get();
                }
            }
            if (max > 0) {
                result.set(max);
                context.write(key, result);
            }
        }
    }
    
    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        conf.set("mapreduce.output.textoutputformat.separator","\t");
        Job job = Job.getInstance(conf, "Q1");
        
        job.setJarByClass(Q1.class);
        job.setMapperClass(TokenMapper.class);
        job.setCombinerClass(IntMaximumReducer.class);
        job.setReducerClass(IntMaximumReducer.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(IntWritable.class);
        
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
