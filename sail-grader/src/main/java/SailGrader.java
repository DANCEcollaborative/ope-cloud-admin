import edu.cmu.scs.cc.grader.Config;
import edu.cmu.scs.cc.grader.GradeWriter;
import edu.cmu.scs.cc.grader.GradingProcessor;

/**
 * @author Jessica
 * @title SailGrader
 * @date 3/30/24 10:36 PM
 * @description This class is the entry point of the SailGrader.
 */
public class SailGrader {
    public static void main(String[] args) {
        // init the config
        Config config = new Config(args);
        // create 1 or more GradeStrategy instance(s)
        config.setEnableDefaultGradeStrategies(false);
        OPEGradeStrategy opeGradeStrategy = new OPEGradeStrategy(config);

        opeGradeStrategy.setNotebookFileBoolColumn("ba4d74d2-0cb8");

        GradingProcessor gradingProcessor = new GradingProcessor(
                config, opeGradeStrategy);

        gradingProcessor.run();
    }

}

