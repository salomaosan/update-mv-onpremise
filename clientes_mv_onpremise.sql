select 
		cli.cdcliente, 
		cli.nmcliente, 
		count(con.cdcontrato) as 'Cloud' 
	from ad_cliente cli 
	inner join fa_clientecontrato fa on fa.cdcliente = cli.cdcliente 
	and fa.fgativo = 'Y' 
	left join fa_contrato con on fa.cdcontrato = con.cdcontrato 
	and con.nmcontrato like '%Cloud%' 
	where cli.nmcliente like '%F.MV%'
	and cli.idativo = 'Y' 
	group by cli.cdcliente, cli.nmcliente
    having count(con.cdcontrato) = 0


    