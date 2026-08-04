"use client";

import { useEffect, useRef } from "react";
import { createChart } from "lightweight-charts";


type Candle = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume?: number;
};


export default function CandleChart({
  data,
}: {
  data: Candle[];
}) {


  const containerRef =
    useRef<HTMLDivElement>(null);



  useEffect(() => {


    if (!containerRef.current)
      return;


    if (!Array.isArray(data) || data.length === 0)
      return;



    // Clear previous chart instance
    containerRef.current.innerHTML = "";



    const chart =
      createChart(
        containerRef.current,
        {

          width:
            containerRef.current.clientWidth || 900,

          height: 500,


          layout: {

            background: {
              color: "#0f172a",
            },

            textColor: "#ffffff",

          },


          grid: {

            vertLines: {
              color: "#1f2937",
            },


            horzLines: {
              color: "#1f2937",
            },

          },


          timeScale: {

            timeVisible: true,

            secondsVisible: false,

          },

        }
      );




    // lightweight-charts 4.2.0 API

    const candleSeries =
      chart.addCandlestickSeries();





    // ----------------------------
    // DATA CLEANING
    // ----------------------------


    const seen =
      new Set<number>();



    const cleaned =

      data

        .map((d) => {


          const timestamp =
            new Date(d.date).getTime();



          return {

            time:
              Math.floor(timestamp / 1000),

            open:
              Number(d.open),

            high:
              Number(d.high),

            low:
              Number(d.low),

            close:
              Number(d.close),

          };

        })



        // remove invalid values

        .filter((d) =>

          Number.isFinite(d.time) &&

          Number.isFinite(d.open) &&

          Number.isFinite(d.high) &&

          Number.isFinite(d.low) &&

          Number.isFinite(d.close)

        )



        // remove duplicate dates

        .filter((d) => {


          if(seen.has(d.time))
            return false;


          seen.add(d.time);

          return true;

        })



        // chart requires ascending order

        .sort(
          (a,b)=>
            a.time - b.time
        );





    console.log(
      "CLEANED CANDLES:",
      cleaned.length
    );



    candleSeries.setData(cleaned);



    chart
      .timeScale()
      .fitContent();





    // Responsive resize

    const resizeObserver =
      new ResizeObserver(() => {


        if(containerRef.current){


          chart.applyOptions({

            width:
              containerRef.current.clientWidth,

          });


        }


      });



    resizeObserver.observe(
      containerRef.current
    );





    return () => {


      resizeObserver.disconnect();


      chart.remove();


    };



  }, [data]);





  return (

    <div

      ref={containerRef}

      style={{

        width: "100%",

        height: 500,

      }}

    />

  );

}
