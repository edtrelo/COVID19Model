using CSV, DataFrames, Plots, DifferentialEquations, Dates

params = CSV.read("D:/Edgar Trejo/Universidad/Proyecto/COVID19Model/data/cleandata/params.csv", DataFrame)

β(t, k) = params[trunc(Int, t)+1, k]

es = CSV.read(download("https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/cleandata/viajes/viajes_es_reg.csv"),
                DataFrame, select = 2:6)

s = CSV.read(download("https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/cleandata/viajes/viajes_s_reg.csv"),
                DataFrame, select = 2:6)

d = CSV.read(download("https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/cleandata/viajes/viajes_d_reg.csv"),
                DataFrame, select = 2:6)

x0df = CSV.read("D:/Edgar Trejo/Universidad/Proyecto/COVID19Model/data/cleandata/x0_reg.csv", DataFrame)
pobdf = CSV.read(download("https://raw.githubusercontent.com/edtrelo/COVID19Model/main/data/cleandata/pob_reg.csv"), DataFrame)

pob = pobdf[!, :pop]

fecha_inicio = Date(2020, 2, 27)
red_traf = 0.7
inicio_red = 25
f = 0.1
# params epidemiológicos
l = 1/3.3
θ = 1/(6.8 - 3.3)
pa, pm, ps = 0.5, 0.476, 0.024
σ = 1/2.4
δ = 1/5.28
ω = 1/4.27
ρ = 1/5
q = 0.0658


viajes = [es, s, d]

function Model(dXdt, X, p, t)
    
    S(i) = X[8*(i-1) + 1]
    E(i) =  X[8*(i-1) + 2]
    Ip(i) = X[8*(i-1) + 3]
    Iss(i) = X[8*(i-1) + 4]
    H(i) = X[8*(i-1) + 5]
    D(i) = X[8*(i-1) + 6]
    Ia(i) = X[8*(i-1) + 7]
    Im(i) = X[8*(i-1) + 8]
    
    red_traf = p

    N(i) = pob[i] - D(i)
    γ(i) = N(i) / pob[i]
    
    function Ω(i, j, d)

        wd = (dayofweek(fecha_inicio) + d )-1  % 7
        if wd == 5
            if i == j
                p = (N(i) - γ(i)*(sum(viajes[2][i, 1:end]) - viajes[2][i, i])) / N(i)
            else
                p = γ(i)*viajes[2][i, j] / N(i)
            end


        elseif wd == 6
            if i == j
                p = (N(i) - γ(i)*(sum(viajes[3][i, 1:end]) - viajes[3][i, i])) / N(i)
            else
                p = γ(i)*viajes[3][i, j] / N(i)
            end

        else
            if i == j
                p = (N(i) - γ(i)*(sum(viajes[1][i, 1:end]) - viajes[1][i, i])) / N(i)
            else
                p = γ(i)*viajes[1][i, j] / N(i) / N(i)
            end
        end

        if d > inicio_red
            p = (1-red_traf)*p
        end

        return p
    end

    L(t, i) = sum([β(t, k)* Ω(i, k, t) * sum([ Ω(m, k, t) * (Ip(m) + Ia(m) + f*Im(m)) for m in 1:5]) for k in 1:5])
            
    for i in 1:5    
        # X_i; los componentes de cada ciudad
        # ecuación de los suceptibles para la ciudad i
        fuerza = L(t, i)
        dXdt[8*(i-1) + 1] = -fuerza*S(i)
        # ecuación de los expuestos para la ciudad i
        dXdt[8*(i-1) + 2] = fuerza*S(i) - l*E(i)
        # ecuación para los pre-infectados
        dXdt[8*(i-1) + 3] = l*E(i) - θ*Ip(i)
        # ecuación para los infectados severos
        dXdt[8*(i-1) + 4] = θ*ps*Ip(i) - ω*Iss(i)
        # ecuación para los hospitalizados
        dXdt[8*(i-1) + 5] = ω*Iss(i) - (1-q)*ρ*H(i) - δ*q*H(i)
        # ecuación de los difuntos
        dXdt[8*(i-1) + 6] = q*δ*H(i)
        # ecuación de los asintomáticos
        dXdt[8*(i-1) + 7] = θ*pa*Ip(i) - σ*Ia(i)
        # ecuación de los mild sym
        dXdt[8*(i-1) + 8] = θ*pm*Ip(i) - σ*Im(i)
    end

    return dXdt
end

x0 = zeros(8*5)
indicesCasos = [1, 5]

for i in 1:5
    if i in indicesCasos
        x0[8*(i-1) + 1: 8*(i-1)+8] = [pob[i]-x0df[i, 2]-x0df[i, 3]-1, x0df[i, 3], x0df[i, 2], 0, 0, 0, 1, 0]
    else
        x0[8*(i-1) + 1: 8*(i-1)+8] = [pob[i]-x0df[i, 2]-x0df[i, 3], x0df[i, 3], x0df[i, 2], 0, 0, 0, 0, 0]
    end
end

reds = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
solsR = []


for r in reds
    tspan = (0.0, 94.0)
    prob = ODEProblem(Model, x0, tspan, r)
    sol = solve(prob, saveat = 0:94)
    append!(solsR, sol)
end

# solución del caso base

@show solsR[1]
plot(solsR[1][1, :])