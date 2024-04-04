import com.google.common.base.Stopwatch;
import edu.cmu.scs.cc.codestyle.CodeStyleChecker;
import edu.cmu.scs.cc.codestyle.model.StyleCheckResult;
import edu.cmu.scs.cc.grader.Config;
import edu.cmu.scs.cc.grader.GradeWriter;
import edu.cmu.scs.cc.grader.strategy.ScoreMapGradeStrategy;

import java.io.File;
import java.io.IOException;
import java.util.HashMap;
import java.util.List;

public class OPEGradeStrategy extends ScoreMapGradeStrategy {
    public Config config;
    public GradeWriter gradeWriter;
    private static final Integer MAX_FILE_NUMBER = 1;

    String notebookFileBoolColumn;
    Boolean notebookBoolColumnExists;


    public OPEGradeStrategy(Config config) {
        this.config = config;
        this.gradeWriter = new GradeWriter(config);
    }

    public HashMap<String, Comparable> grade() {
        String reportExists = "false";

        File reportFile = new File(config.getSubmissionFolder() + "./workspace/workspace.ipynb");
        boolean fileExists = reportFile.exists();
        if(fileExists) {
            gradeWriter.writeLog("Found workspace.ipynb\n");
            reportExists = "true";
        }
        else {
            gradeWriter.writeLog("workspace.ipynb file is not found\n");
        }
        this.studentScores.put(this.notebookFileBoolColumn, reportExists);
        return this.studentScores;
    }

    public Config getConfig() {
        return this.config;
    }

    public GradeWriter getGradeWriter() {
        return this.gradeWriter;
    }

    public String getNotebookFileBoolColumn() {
        return notebookFileBoolColumn;
    }

    public void setNotebookFileBoolColumn(String notebookFileBoolColumn) {
        this.notebookFileBoolColumn = notebookFileBoolColumn;
    }

    public void setNotebookFileBoolColumnExists(Boolean notebookBoolColumnExists) {
        this.notebookBoolColumnExists = notebookBoolColumnExists;
    }
}

