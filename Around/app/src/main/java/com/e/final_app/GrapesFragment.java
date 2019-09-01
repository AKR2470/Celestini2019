package com.e.final_app;

import android.graphics.Color;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.fragment.app.Fragment;

import com.mikhaellopez.circularprogressbar.CircularProgressBar;

//import android.support.v4.app.Fragment;

public class GrapesFragment extends Fragment {

    public GrapesFragment() {
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
        View v= inflater.inflate(R.layout.fragment_grapes, container, false);
        circularProgressBar = v.findViewById(R.id.circularProgressBarpm);
        text = v.findViewById(R.id.textViewpm);
        for(int i=0;i<5;i++){
            circularProgressBar.setProgressWithAnimation(20f, Long.valueOf(2000)); // =1s
           text.setText(String.valueOf(20*i));
        }


// Set Progress Max
        circularProgressBar.setProgressMax(100f);

// Set ProgressBar Color
        circularProgressBar.setProgressBarColor(Color.BLACK);

// Set background ProgressBar Color
        circularProgressBar.setBackgroundProgressBarColor(Color.GRAY);

// Set Width
        circularProgressBar.setProgressBarWidth(7f); // in DP
        circularProgressBar.setBackgroundProgressBarWidth(3f); // in DP

// Other
        circularProgressBar.setRoundBorder(true);
        circularProgressBar.setStartAngle(180f);
        circularProgressBar.setProgressDirection(CircularProgressBar.ProgressDirection.TO_RIGHT);
        return v;
    }
    public void setValue(double pm25) {
        Log.d("msg",String.valueOf(pm25));
        text.setText(String.format("%.1f", pm25)+ "ug/m3");
        float d = (float)(pm25/200) * 100;
        circularProgressBar.setProgressWithAnimation(d, Long.valueOf(1000)); // =1s
    }
}
