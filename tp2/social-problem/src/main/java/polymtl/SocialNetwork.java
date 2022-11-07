package polymtl;

import java.io.IOException;
import java.util.*;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class SocialNetwork {

    public static class RecommendationMapper
            extends Mapper<LongWritable, Text, IntWritable, Recommendation> {

        public void map(LongWritable key, Text value, Context context
        ) throws IOException, InterruptedException {
            // Parse user ID and friends list
            String[] line = value.toString().split("\t");
            Integer user = Integer.parseInt(line[0]);
            ArrayList<Integer> friends = new ArrayList<Integer>();
            if (line.length > 1) {
                for (String rawFriend : line[1].split(",")) {
                    Integer friend = Integer.parseInt(rawFriend);
                    friends.add(friend);
                    // Write a recommendation with -1 as mutual friend to indicate that this
                    // recommendation is a direct friend and can then be omitted in the reduce step
                    context.write(new IntWritable(user), new Recommendation(friend, -1));
                }
            }
            // Writes recommendations in both ways for each pair of friends
            for ( Integer a : friends ) {
                for ( Integer b : friends ) {
                    if (a != b) {
                        context.write(new IntWritable(a), new Recommendation(b, user));
                        context.write(new IntWritable(b), new Recommendation(a, user));
                    }
                }
            }
        }
    }

    public static class RecommendationReducer
            extends Reducer<IntWritable, Recommendation, IntWritable, Text> {

        public void reduce(IntWritable key, Iterable<Recommendation> recs,
                           Context context
        ) throws IOException, InterruptedException {

            // Create a with the count of every recommendation and a list of user's friends
            HashMap<Integer, Integer> recommendations = new HashMap<>();
            ArrayList<Integer> friends = new ArrayList<>();
            for (Recommendation rec : recs) {
                if (rec.mutualFriend != -1) {
                    recommendations.merge(rec.recommendedUser, 1, Integer::sum);
                } else {
                    friends.add(rec.recommendedUser);
                }
            }

            // This comparator allows us the sort by reverse key, then by value
            Comparator<Map.Entry<Integer, Integer>> reverseValThenKeyComp =
                    Map.Entry.<Integer, Integer>comparingByValue().reversed()
                            .thenComparing(Map.Entry.<Integer, Integer>comparingByKey());
            ArrayList<String> finalRecommendations = new ArrayList<>();

            // Create the recommendation list
            recommendations.entrySet().stream()
                    // Only keep recommended user if it is not already friend with the user
                    .filter(entry -> !friends.contains(entry.getKey()))
                    // Sort by recommendation count, then by user ID
                    .sorted(reverseValThenKeyComp)
                    // Keep 10 first entries
                    .limit(10)
                    // Add it to the final recommendations list
                    .forEach(entry -> {
                        finalRecommendations.add(entry.getKey().toString());
                    });

            // Write the recommendation
            context.write(key, new Text(String.join(",", finalRecommendations)));

        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(SocialNetwork.class);
        job.setMapperClass(RecommendationMapper.class);
        job.setReducerClass(RecommendationReducer.class);
        job.setMapOutputKeyClass(IntWritable.class);
        job.setMapOutputValueClass(Recommendation.class);
        job.setOutputKeyClass(IntWritable.class);
        job.setOutputValueClass(Text.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}