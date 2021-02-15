for f in ~/erda/kiehn_lab/nathalie/fasting_compressed/*
do for g in $f/*
    do 
        python main.py --data $g/ --label_video --analyze_video
    done
done
