package com.e.final_app;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.fragment.app.Fragment;

import com.mikhaellopez.circularprogressbar.CircularProgressBar;

import static android.content.Intent.getIntent;

//import android.support.v4.app.Fragment;

public class AppleFragment extends Fragment {

    public AppleFragment() {
        // Required empty public constructor
    }

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

    }
    CircularProgressBar circularProgressBar;
    TextView text;
    @Override
    public View onCreateView(LayoutInflater inflater, ViewGroup container,
                             Bundle savedInstanceState) {
        // Inflate the layout for this fragment
        View v= inflater.inflate(R.layout.fragment_apple, container, false);
        circularProgressBar = v.findViewById(R.id.circularProgressBarNO2);
        text = v.findViewById(R.id.textViewNO2);
//        Intent k =  getIntent();
//        double value = getIntent().getDoubleExtra("NO2",0);
//        text.setText(String.valueOf(value));
        ////for(int i=0;i<5;i++){
            circularProgressBar.setProgressWithAnimation(20f, Long.valueOf(2000)); // =1s

       // }


// Set Progress Max
        circularProgressBar.setProgressMax(100f);

// Set ProgressBar Color
        circularProgressBar.setProgressBarColor(Color.BLACK);
// or with gradient
        // circularProgressBar.setProgressBarColorStart(Color.GREEN);
        //  circularProgressBar.setProgressBarColorEnd(Color.RED);
        // circularProgressBar.setProgressBarColorDirection(CircularProgressBar.GradientDirection.TOP_TO_BOTTOM);

// Set background ProgressBar Color
        circularProgressBar.setBackgroundProgressBarColor(Color.GRAY);
// or with gradient
//        circularProgressBar.setBackgroundProgressBarColorStart(Color.WHITE);
//        circularProgressBar.setBackgroundProgressBarColorEnd(Color.WHITE);
//        circularProgressBar.setBackgroundProgressBarColorDirection(CircularProgressBar.GradientDirection.TOP_TO_BOTTOM);

// Set Width
        circularProgressBar.setProgressBarWidth(7f); // in DP
        circularProgressBar.setBackgroundProgressBarWidth(3f); // in DP

// Other
        circularProgressBar.setRoundBorder(true);
        circularProgressBar.setStartAngle(180f);
        circularProgressBar.setProgressDirection(CircularProgressBar.ProgressDirection.TO_RIGHT);
        return v;
    }

    public void setValue(double no2) {
        Log.d("msg",String.valueOf(no2));
        text.setText(String.format("%.1f", no2)+ "ug/m3");
        float d = (float)(no2/150) * 100;
        circularProgressBar.setProgressWithAnimation(d, Long.valueOf(1000)); // =1s
    }

}
