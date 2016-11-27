/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.omrow.stemmeing;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.Locale;
import morfologik.stemming.WordData;
import morfologik.stemming.polish.PolishStemmer;

/**
 *
 * @author Ola1
 */
public class Main {
    public static void main(String [] args) throws FileNotFoundException, IOException {
        PolishStemmer stemmer = new PolishStemmer();
        
        File folder = new File("C:/Users/Ola1/Desktop/nlp/books/");
        File[] listOfFiles = folder.listFiles();
        BufferedReader br;
        PrintWriter writer;
                
        for (File file : listOfFiles) {
            if (file.isFile()) {
                br = new BufferedReader(new FileReader(file.getAbsolutePath()));
                writer = new PrintWriter("C:/Users/Ola1/Desktop/nlp/books stem/"+file.getName(), "UTF-8");
               
                //usuwam cztery pierwsze linijki, bo moga byc jakies nazwiska, tytuly itp.
                for (int i = 0; i < 4; i++) {
                    br.readLine();
                }
                
                String line = br.readLine();
                while(line != null) {
                    for (String t : line.toLowerCase(new Locale("pl")).split("[\\s\\.\\,]+")) {
                        for (WordData wd : stemmer.lookup(t)) {
                            writer.println(wd.getStem());
                        }
                    }
                    line = br.readLine();
                }
                writer.close();
            }
        }
    }
}
