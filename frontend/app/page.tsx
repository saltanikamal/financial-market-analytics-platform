"use client";

import { useEffect, useState } from "react";
import Header from "@/components/dashboard/Header";
import CandleChart from "@/components/charts/CandleChart";

const API_BASE = "http://localhost:8000";

const STOCKS = [
  "AAPL",
  "MSFT",
  "NVDA",
  "SPY",
];

type Signal = "BUY" | "SELL" | "HOLD";

type Candle = {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
};


export default function Dashboard() {


  const [symbol, setSymbol] =
    useState("AAPL");


  const [signal, setSignal] =
    useState<Signal>("HOLD");


  const [latestPrice, setLatestPrice] =
    useState<number | null>(null);


  const [prediction, setPrediction] =
    useState<any>(null);


  const [dataMessage, setDataMessage] =
    useState("");


  const [chartData, setChartData] =
    useState<Candle[]>([]);



  // ============================
  // LOAD PRICE DATA
  // ============================

  useEffect(() => {


    async function loadChart(){


      try {


        const response =
          await fetch(
            `${API_BASE}/analytics/ohlc/${symbol}`
          );


        const result =
          await response.json();



        if(!result.available){

          setDataMessage(result.message);

          setChartData([]);

          return;

        }



        setDataMessage("");



        const data =
          result.data;



        const candles =
          data.map((d:any)=>({

            date:
              String(d.date)
              .split("T")[0],


            open:
              Number(d.open),


            high:
              Number(d.high),


            low:
              Number(d.low),


            close:
              Number(d.close)

          }));



        setChartData(candles);



        const last =
          data[data.length - 1];



        if(last){


          setLatestPrice(
            Number(last.close)
          );



          const lastMA7 =
            Number(last.ma7);


          const lastMA20 =
            Number(last.ma20);



          if(lastMA7 > lastMA20)

            setSignal("BUY");


          else if(lastMA7 < lastMA20)

            setSignal("SELL");


          else

            setSignal("HOLD");

        }



      }


      catch(error){

        console.error(error);

      }


    }



    loadChart();



  },[symbol]);





  // ============================
  // LOAD ML PREDICTION
  // ============================


  useEffect(()=>{


    async function loadPrediction(){


      try{


        const response =
          await fetch(
            `${API_BASE}/predict/${symbol}`
          );



        if(!response.ok){

          setPrediction(null);

          return;

        }



        const result =
          await response.json();



        setPrediction(result);


      }


      catch(error){

        console.error(error);

        setPrediction(null);

      }


    }



    loadPrediction();


  },[symbol]);





  return (

    <div
      className="
      min-h-screen
      bg-slate-950
      text-white
      p-6
      "
    >


      <Header />



      <h1
        className="
        text-3xl
        font-bold
        mb-6
        "
      >

        Financial Intelligence Dashboard

      </h1>





      <select

        className="
        bg-slate-800
        rounded
        p-2
        mb-5
        "

        value={symbol}

        onChange={
          (e)=>
          setSymbol(e.target.value)
        }

      >

        {
          STOCKS.map((stock)=>(

            <option
              key={stock}
              value={stock}
            >

              {stock}

            </option>

          ))
        }


      </select>






      <div

        className={`
        rounded-lg
        p-4
        mb-5
        w-fit

        ${
          signal==="BUY"
          ?
          "bg-green-600"
          :
          signal==="SELL"
          ?
          "bg-red-600"
          :
          "bg-yellow-500"
        }

        `}

      >

        <h2
          className="font-bold text-lg"
        >

          Market Signal

        </h2>


        <p>
          Signal: {signal}
        </p>


        {
          latestPrice !== null &&

          <p>
            Price: ${latestPrice.toFixed(2)}
          </p>

        }


      </div>





      <div

        className="
        bg-slate-800
        rounded-lg
        p-5
        mb-5
        w-fit
        "

      >

        <h2
          className="font-bold mb-3"
        >

          ML Prediction

        </h2>


        {
          prediction ?

          <div>

            <p>
              Signal: {prediction.signal}
            </p>


            <p>
              Confidence: {prediction.confidence}
            </p>


            <p>
              Probability: {prediction.probability}
            </p>


          </div>


          :

          <p>
            No prediction available
          </p>

        }


      </div>





      {
        dataMessage &&

        <div
          className="
          bg-red-700
          rounded
          p-3
          mb-5
          "
        >

          {dataMessage}

        </div>

      }






      <div
        className="
        w-full
        rounded-lg
        bg-slate-900
        "
      >

        <CandleChart
          data={chartData}
        />


      </div>



    </div>

  );


}
