package polymtl;

import org.apache.hadoop.io.Writable;

import java.io.DataInput;
import java.io.DataOutput;
import java.io.IOException;



public class Recommendation implements Writable {
    public Integer recommendedUser;
    public Integer mutualFriend;



    /**
    * Recommendation Constructor.
    * This function creates a Recommendation.
    *
    * @param recommendedUser    The recommended user ID
    * @param mutualFriend       The mutual friend ID that the associated user has with the mutual friend.
    *                           If -1 is provided, this means that the associated user is direct friend
    *                           of the recommended user. This type of recommendation is useful to
    *                           filter false/positive recommendation in the reduce step to avoid
    *                           recommending a user to someone who is already friend with.
    */
    public Recommendation(Integer recommendedUser, Integer mutualFriend) {
        this.recommendedUser = recommendedUser;
        this.mutualFriend = mutualFriend;
    }

    /**
    * Recommendation Constructor.
    * This create an empty Recommendation.
    */
    public Recommendation() {
        this.recommendedUser = -1;
        this.mutualFriend = -1;
    }

    /**
    * Write the Recommendation on a DataOutput.
    *
    * @param output The output to write to.
    */
    @Override
    public void write(DataOutput output) throws IOException {
        output.writeInt(recommendedUser);
        output.writeInt(mutualFriend);
    }

    /**
    * Fills all the Recommendation fields by reading a DataInput.
    *
    * @param input The input to read from.
    */
    @Override
    public void readFields(DataInput input) throws IOException {
        recommendedUser = input.readInt();
        mutualFriend = input.readInt();
    }
}
