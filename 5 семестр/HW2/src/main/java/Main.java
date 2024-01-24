import java.io.File;
import java.io.PrintWriter;
import java.util.List;


public class Main {
    public static void main(String[] args) throws Exception {
        List<Tree> trees = TreeBuilder.readTreesFromDB(new H2Connection());
        int totalLeaves = TreeBuilder.getTotalLeaves(trees);
        try (PrintWriter out = new PrintWriter(new File("output.csv"))) {
            out.println(totalLeaves);
        }
    }
}