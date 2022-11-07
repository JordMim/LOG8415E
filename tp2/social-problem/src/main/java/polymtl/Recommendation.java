package polymtl;

import org.apache.hadoop.io.Writable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;

public class Recommendation implements Writable {
    public Integer recommendedUser;
    public Integer mutualFriend;

    /**
     * Recommendation Constructor
     * @param recommendedUser The recommended user ID
     * @param mutualFriend The mutual friend (if this is -1, it means that you are friend with the said user)
     * Builds a Recommendation object with the specified parameters
     */
    public Recommendation(Integer recommendedUser, Integer mutualFriend) {
        this.recommendedUser = recommendedUser;
        this.mutualFriend = mutualFriend;
    }

    public Recommendation() {
        this.recommendedUser = -1;
        this.mutualFriend = -1;
    }

    /**
     * @param output the output to be written to
     * Writes two saved value to an output
     */
    @Override
    public void write(DataOutput output) throws IOException {
        output.writeInt(recommendedUser);
        output.writeInt(mutualFriend);
    }

    /**
     * @param input  the input to be red
     * Reads the two fields of an input and stores them
     */
    @Override
    public void readFields(DataInput input) throws IOException {
        recommendedUser = input.readInt();
        mutualFriend = input.readInt();
    }
}
