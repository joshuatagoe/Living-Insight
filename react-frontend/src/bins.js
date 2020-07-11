

function get_mental_health_bin(x){
    if(x <2.67){
        return 0;
    }
    if(x<5.34){
        return 2.67;
    }
    if(x<8.01){
        return 5.34;
    }
    if(x<10.68){
        return 8.01;
    }
    if(x<13.35){
        return 10.68
    }
    if(x<16.02){
        return 13.35
    }
    if(x<18.69){
        return 16.02
    }
    if(x<21.36){
        return 18.69
    }
    return 21.36;
}

function get_subway_bin(x){
    if(x<28){
        return 0;
    }
    if(x<56){
        return 28;
    }
    if(x<84){
        return 56;
    }
    if(x<112){
        return 84;
    }
    if(x<140){
        return 112;
    }
    if(x<168){
        return 140;
    }
    if(x<196){
        return 168;
    }
    if(x<224){
        return 196
    }
    if(x<252){
        return 224;
    }
    if(x<280){
        return 252;
    }
    if(x<308){
        return 280;
    }
    if(x<336){
        return 308;
    }
    if(x<364){
        return 336;
    }
    if(x<392){
        return 364;
    }
    if(x<420){
        return 392;
    }
    if(x<448){
        return 420; 
    }
    if(x<476){
        return 448;
    }
    if(x<504){
        return 476;
    }
    if(x<532){
        return 504;
    }
    if(x<560){
        return 532;
    }
    if(x<588){
        return 560;
    }
    if(x<616){
        return 580;
    }
    if(x<644){
        return 616;
    }
    return 644;
}

function get_felonies_bin(x){
    for(let i = 1; i<=24;i++){
        if(x<55*i){
            return 55*(i-1);
        }
    }
    
    return 55*24;

}

function get_violations_bin(x){
    for(let i = 1; i<=22;i++){
        if(x<39*i){
            return 39*(i-1);
        }
    }
    return 39*22;
}

function get_misdemeanors_bin(x){
    for(let i = 1; i<=25;i++){
        if(x<94*i){
            return 94*(i-1);
        }
    }
    return 94*25;
}

function get_collissions_bin(x){
    for(let i = 1; i<=32;i++){
        if(x<7790*i){
            return 7790*(i-1);
        }
    }
    return 7790*32;

}

function get_num_injured_bin(x){
    for(let i = 1; i<=32;i++){
        if(x<1313*i){
            return 1313*(i-1);
        }
    }
    return 1313*32;

}

function get_num_killed_bin(x){
    for(let i = 1; i<=16;i++){
        if(x<10.6*i){
            return 10.6*(i-1);
        }
    }
    return 10.6*16;

}

function get_total_affected_bin(x){
    for(let i = 1; i<=32;i++){
        if(x<1321*i){
            return 1321*(i-1);
        }
    }
    return 1321*32;
}

module.exports = {
    get_mental_health_bin,
    get_subway_bin,
    get_collissions_bin,
    get_num_injured_bin,
    get_num_killed_bin,
    get_total_affected_bin,
    get_felonies_bin,
    get_violations_bin,
    get_misdemeanors_bin,
}

