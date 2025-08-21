module.exports = {
    apps:[
        {
            name:"fs",
            script: "uvicorn",
            args:"index:app --host 0.0.0.0 --port 8000",
            interpreter:"python3",
            watch:false,
            env:{}
        }
    ]
}