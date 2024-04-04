import edu.cmu.scs.cc.grader.Config;
import edu.cmu.scs.cc.grader.GradeWriter;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.powermock.core.classloader.annotations.PowerMockIgnore;
import org.powermock.modules.junit4.PowerMockRunner;

import java.nio.file.Paths;
import java.util.HashMap;
/**
 * @author Jessica
 * @title SailGraderTest
 * @date 3/30/24 10:50 PM
 * @description This class is the test class for SailGrader.
 */
@RunWith(PowerMockRunner.class)
@PowerMockIgnore({"javax.net.ssl.*"})
public class SailGraderTest {
    private OPEGradeStrategy strategy;

    private static String globalPath = Paths.get("src", "test", "resources").toString();

    @Mock
    private Config config;

    @Mock
    private static GradeWriter gradeWriter;

    public void stubMethodsWithTestFolder(String testFolder) {
        // use Mockito to set the submission folder during unit test
        // in order to read from the test sample submission folder
        Mockito.when(config.getSubmissionFolder()).thenReturn(Paths.get(globalPath, testFolder).toFile().getAbsolutePath() + "/");
        // write to a local "feedback" file under the test sample submission folder
        Mockito.when(config.getFeedbackFile()).thenReturn("feedback");
        // write to a local "log" file under the test sample submission folder
        Mockito.when(config.getLogFile()).thenReturn("log");
        strategy = new OPEGradeStrategy(config);
        strategy.setNotebookFileBoolColumn("ba4d74d2-0cb8");
    }

    @Test
    public void testGradeValid() {
        stubMethodsWithTestFolder("pass");
        HashMap<String, Comparable> score = strategy.grade();
        Assert.assertEquals("true", score.get("ba4d74d2-0cb8"));
    }

    @Test
    public void testGradeInvalid() {
        stubMethodsWithTestFolder("fail");
        HashMap<String, Comparable> score = strategy.grade();
        Assert.assertEquals("false", score.get("ba4d74d2-0cb8"));
    }
}
